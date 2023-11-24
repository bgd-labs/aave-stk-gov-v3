// SPDX-License-Identifier: agpl-3.0
pragma solidity ^0.8.0;

import {IERC20} from 'openzeppelin-contracts/contracts/token/ERC20/IERC20.sol';
import {IERC20Metadata} from 'openzeppelin-contracts/contracts/token/ERC20/extensions/IERC20Metadata.sol';
import {BaseDelegation} from 'aave-token-v3/BaseDelegation.sol';

import {SafeERC20} from 'openzeppelin-contracts/contracts/token/ERC20/utils/SafeERC20.sol';
import {IStakedTokenV2} from '../interfaces/IStakedTokenV2.sol';
import {StakedTokenV2} from './StakedTokenV2.sol';
import {IStakedTokenV3} from '../interfaces/IStakedTokenV3.sol';
import {PercentageMath} from '../lib/PercentageMath.sol';
import {RoleManager} from '../utils/RoleManager.sol';
import {IERC20Permit} from 'openzeppelin-contracts/contracts/token/ERC20/extensions/IERC20Permit.sol';
import {SafeCast} from 'openzeppelin-contracts/contracts/utils/math/SafeCast.sol';
import {IRewardsController} from 'lib/aave-v3-periphery/contracts/rewards/interfaces/IRewardsController.sol';

/**
 * @title StakedTokenV3
 * @notice Contract to stake Aave token, tokenize the position and get rewards, inheriting from a distribution manager contract
 * @author BGD Labs
 */
contract StakedTokenV3 is
  StakedTokenV2,
  IStakedTokenV3,
  RoleManager,
  BaseDelegation
{
  using SafeERC20 for IERC20;
  using PercentageMath for uint256;
  using SafeCast for uint256;
  using SafeCast for uint104;

  uint256 public constant SLASH_ADMIN_ROLE = 0;
  uint256 public constant COOLDOWN_ADMIN_ROLE = 1;
  uint256 public constant CLAIM_HELPER_ROLE = 2;
  uint216 public constant INITIAL_EXCHANGE_RATE = 1e18;
  uint256 public constant EXCHANGE_RATE_UNIT = 1e18;

  /// @notice lower bound to prevent spam & avoid exchangeRate issues
  // as returnFunds can be called permissionless an attacker could spam returnFunds(1) to produce exchangeRate snapshots making voting expensive
  uint256 public immutable LOWER_BOUND;

  IRewardsController public immutable REWARDS_CONTROLLER;

  // Reserved storage space to allow for layout changes in the future.
  uint256[6] private ______gap;
  /// @notice Seconds between starting cooldown and being able to withdraw
  uint256 internal _cooldownSeconds;
  /// @notice The maximum amount of funds that can be slashed at any given time
  uint256 internal _maxSlashablePercentage;
  /// @notice Mirror of latest snapshot value for cheaper access
  uint216 internal _currentExchangeRate;
  /// @notice Flag determining if there's an ongoing slashing event that needs to be settled
  bool public inPostSlashingPeriod;

  modifier onlySlashingAdmin() {
    require(
      msg.sender == getAdmin(SLASH_ADMIN_ROLE),
      'CALLER_NOT_SLASHING_ADMIN'
    );
    _;
  }

  modifier onlyCooldownAdmin() {
    require(
      msg.sender == getAdmin(COOLDOWN_ADMIN_ROLE),
      'CALLER_NOT_COOLDOWN_ADMIN'
    );
    _;
  }

  modifier onlyClaimHelper() {
    require(
      msg.sender == getAdmin(CLAIM_HELPER_ROLE),
      'CALLER_NOT_CLAIM_HELPER'
    );
    _;
  }

  constructor(
    IERC20 stakedToken,
    uint256 unstakeWindow,
    IRewardsController rewardsController
  ) StakedTokenV2(stakedToken, unstakeWindow) {
    uint256 decimals = IERC20Metadata(address(stakedToken)).decimals();
    LOWER_BOUND = 10 ** decimals;
    REWARDS_CONTROLLER = rewardsController;
  }

  function initialize(
    address slashingAdmin,
    address cooldownPauseAdmin,
    address claimHelper,
    uint256 maxSlashablePercentage,
    uint256 cooldownSeconds
  ) internal initializer {
    InitAdmin[] memory initAdmins = new InitAdmin[](3);
    initAdmins[0] = InitAdmin(SLASH_ADMIN_ROLE, slashingAdmin);
    initAdmins[1] = InitAdmin(COOLDOWN_ADMIN_ROLE, cooldownPauseAdmin);
    initAdmins[2] = InitAdmin(CLAIM_HELPER_ROLE, claimHelper);

    _initAdmins(initAdmins);

    _setMaxSlashablePercentage(maxSlashablePercentage);
    _setCooldownSeconds(cooldownSeconds);
    _updateExchangeRate(INITIAL_EXCHANGE_RATE);
  }

  /// @inheritdoc IStakedTokenV3
  function previewStake(uint256 assets) public view returns (uint256) {
    return (assets * _currentExchangeRate) / EXCHANGE_RATE_UNIT;
  }

  /// @inheritdoc IStakedTokenV2
  function stake(
    address to,
    uint256 amount
  ) external override(IStakedTokenV2, StakedTokenV2) {
    _stake(msg.sender, to, amount);
  }

  /// @inheritdoc IStakedTokenV3
  function stakeWithPermit(
    uint256 amount,
    uint256 deadline,
    uint8 v,
    bytes32 r,
    bytes32 s
  ) external override {
    try
      IERC20Permit(address(STAKED_TOKEN)).permit(
        msg.sender,
        address(this),
        amount,
        deadline,
        v,
        r,
        s
      )
    {
      // do nothing
    } catch (bytes memory) {
      // do nothing
    }
    _stake(msg.sender, msg.sender, amount);
  }

  /// @inheritdoc IStakedTokenV2
  function cooldown() external override(IStakedTokenV2, StakedTokenV2) {
    _cooldown(msg.sender);
  }

  /// @inheritdoc IStakedTokenV3
  function cooldownOnBehalfOf(address from) external override onlyClaimHelper {
    _cooldown(from);
  }

  function _cooldown(address from) internal {
    uint256 amount = balanceOf(from);
    require(amount != 0, 'INVALID_BALANCE_ON_COOLDOWN');
    stakersCooldowns[from] = CooldownSnapshot({
      timestamp: uint40(block.timestamp),
      amount: uint216(amount)
    });

    emit Cooldown(from, amount);
  }

  /// @inheritdoc IStakedTokenV2
  function redeem(
    address to,
    uint256 amount
  ) external override(IStakedTokenV2, StakedTokenV2) {
    _redeem(msg.sender, to, amount.toUint104());
  }

  /// @inheritdoc IStakedTokenV3
  function redeemOnBehalf(
    address from,
    address to,
    uint256 amount
  ) external override onlyClaimHelper {
    _redeem(from, to, amount.toUint104());
  }

  /// @inheritdoc IStakedTokenV3
  function getExchangeRate() public view override returns (uint216) {
    return _currentExchangeRate;
  }

  /// @inheritdoc IStakedTokenV3
  function previewRedeem(
    uint256 shares
  ) public view override returns (uint256) {
    return (EXCHANGE_RATE_UNIT * shares) / _currentExchangeRate;
  }

  /// @inheritdoc IStakedTokenV3
  function slash(
    address destination,
    uint256 amount
  ) external override onlySlashingAdmin returns (uint256) {
    require(!inPostSlashingPeriod, 'PREVIOUS_SLASHING_NOT_SETTLED');
    require(amount > 0, 'ZERO_AMOUNT');
    uint256 currentShares = totalSupply();
    uint256 balance = previewRedeem(currentShares);

    uint256 maxSlashable = balance.percentMul(_maxSlashablePercentage);

    if (amount > maxSlashable) {
      amount = maxSlashable;
    }
    require(balance - amount >= LOWER_BOUND, 'REMAINING_LT_MINIMUM');

    inPostSlashingPeriod = true;
    _updateExchangeRate(_getExchangeRate(balance - amount, currentShares));

    STAKED_TOKEN.safeTransfer(destination, amount);

    emit Slashed(destination, amount);
    return amount;
  }

  /// @inheritdoc IStakedTokenV3
  function returnFunds(uint256 amount) external override {
    require(amount >= LOWER_BOUND, 'AMOUNT_LT_MINIMUM');
    uint256 currentShares = totalSupply();
    require(currentShares >= LOWER_BOUND, 'SHARES_LT_MINIMUM');
    uint256 assets = previewRedeem(currentShares);
    _updateExchangeRate(_getExchangeRate(assets + amount, currentShares));

    STAKED_TOKEN.safeTransferFrom(msg.sender, address(this), amount);
    emit FundsReturned(amount);
  }

  /// @inheritdoc IStakedTokenV3
  function settleSlashing() external override onlySlashingAdmin {
    inPostSlashingPeriod = false;
    emit SlashingSettled();
  }

  /// @inheritdoc IStakedTokenV3
  function setMaxSlashablePercentage(
    uint256 percentage
  ) external override onlySlashingAdmin {
    _setMaxSlashablePercentage(percentage);
  }

  /// @inheritdoc IStakedTokenV3
  function getMaxSlashablePercentage()
    external
    view
    override
    returns (uint256)
  {
    return _maxSlashablePercentage;
  }

  /// @inheritdoc IStakedTokenV3
  function setCooldownSeconds(
    uint256 cooldownSeconds
  ) external onlyCooldownAdmin {
    _setCooldownSeconds(cooldownSeconds);
  }

  /// @inheritdoc IStakedTokenV3
  function getCooldownSeconds() external view returns (uint256) {
    return _cooldownSeconds;
  }

  /// @inheritdoc IStakedTokenV3
  function COOLDOWN_SECONDS() external view returns (uint256) {
    return _cooldownSeconds;
  }

  /**
   * @dev sets the max slashable percentage
   * @param percentage must be strictly lower 100% as otherwise the exchange rate calculation would result in 0 division
   */
  function _setMaxSlashablePercentage(uint256 percentage) internal {
    require(
      percentage < PercentageMath.PERCENTAGE_FACTOR,
      'INVALID_SLASHING_PERCENTAGE'
    );

    _maxSlashablePercentage = percentage;
    emit MaxSlashablePercentageChanged(percentage);
  }

  /**
   * @dev sets the cooldown seconds
   * @param cooldownSeconds the new amount of cooldown seconds
   */
  function _setCooldownSeconds(uint256 cooldownSeconds) internal {
    _cooldownSeconds = cooldownSeconds;
    emit CooldownSecondsChanged(cooldownSeconds);
  }

  /**
   * @dev Allows staking a specified amount of STAKED_TOKEN
   * @param to The address to receiving the shares
   * @param amount The amount of assets to be staked
   */
  function _stake(address from, address to, uint256 amount) internal {
    require(!inPostSlashingPeriod, 'SLASHING_ONGOING');
    require(amount != 0, 'INVALID_ZERO_AMOUNT');

    uint256 balanceOfTo = balanceOf(to);

    REWARDS_CONTROLLER.handleAction(to, totalSupply(), balanceOfTo);

    uint256 sharesToMint = previewStake(amount);

    STAKED_TOKEN.safeTransferFrom(from, address(this), amount);

    _mint(to, sharesToMint.toUint104());

    emit Staked(from, to, amount, sharesToMint);
  }

  /**
   * @dev Redeems staked tokens, and stop earning rewards
   * @param from Address to redeem from
   * @param to Address to redeem to
   * @param amount Amount to redeem
   */
  function _redeem(address from, address to, uint104 amount) internal {
    require(amount != 0, 'INVALID_ZERO_AMOUNT');

    CooldownSnapshot memory cooldownSnapshot = stakersCooldowns[from];
    if (!inPostSlashingPeriod) {
      require(
        (block.timestamp >= cooldownSnapshot.timestamp + _cooldownSeconds),
        'INSUFFICIENT_COOLDOWN'
      );
      require(
        (block.timestamp - (cooldownSnapshot.timestamp + _cooldownSeconds) <=
          UNSTAKE_WINDOW),
        'UNSTAKE_WINDOW_FINISHED'
      );
    }

    uint256 balanceOfFrom = balanceOf(from);
    uint256 maxRedeemable = inPostSlashingPeriod
      ? balanceOfFrom
      : cooldownSnapshot.amount;
    require(maxRedeemable != 0, 'INVALID_ZERO_MAX_REDEEMABLE');

    uint256 amountToRedeem = (amount > maxRedeemable) ? maxRedeemable : amount;

    REWARDS_CONTROLLER.handleAction(from, totalSupply(), balanceOfFrom);

    uint256 underlyingToRedeem = previewRedeem(amountToRedeem);

    _burn(from, amountToRedeem.toUint104());

    if (cooldownSnapshot.timestamp != 0) {
      if (cooldownSnapshot.amount - amountToRedeem == 0) {
        delete stakersCooldowns[from];
      } else {
        stakersCooldowns[from].amount =
          stakersCooldowns[from].amount -
          amountToRedeem.toUint184();
      }
    }

    IERC20(STAKED_TOKEN).safeTransfer(to, underlyingToRedeem);

    emit Redeem(from, to, underlyingToRedeem, amountToRedeem);
  }

  /**
   * @dev Updates the exchangeRate and emits events accordingly
   * @param newExchangeRate the new exchange rate
   */
  function _updateExchangeRate(uint216 newExchangeRate) internal virtual {
    require(newExchangeRate != 0, 'ZERO_EXCHANGE_RATE');
    _currentExchangeRate = newExchangeRate;
    emit ExchangeRateChanged(newExchangeRate);
  }

  /**
   * @dev calculates the exchange rate based on totalAssets and totalShares
   * @dev always rounds up to ensure 100% backing of shares by rounding in favor of the contract
   * @param totalAssets The total amount of assets staked
   * @param totalShares The total amount of shares
   * @return exchangeRate as 18 decimal precision uint216
   */
  function _getExchangeRate(
    uint256 totalAssets,
    uint256 totalShares
  ) internal pure returns (uint216) {
    return
      (((totalShares * EXCHANGE_RATE_UNIT) + totalAssets - 1) / totalAssets)
        .toUint216();
  }

  function _transfer(
    address from,
    address to,
    uint256 amount
  ) internal override {
    uint256 balanceOfFrom = balanceOf(from);
    // Sender
    REWARDS_CONTROLLER.handleAction(from, totalSupply(), balanceOfFrom);

    // Recipient
    if (from != to) {
      uint256 balanceOfTo = balanceOf(to);
      REWARDS_CONTROLLER.handleAction(to, totalSupply(), balanceOfTo);

      CooldownSnapshot memory previousSenderCooldown = stakersCooldowns[from];
      if (previousSenderCooldown.timestamp != 0) {
        // if cooldown was set and whole balance of sender was transferred - clear cooldown
        if (balanceOfFrom == amount) {
          delete stakersCooldowns[from];
        } else if (balanceOfFrom - amount < previousSenderCooldown.amount) {
          stakersCooldowns[from].amount = uint216(balanceOfFrom - amount);
        }
      }
    }

    super._transfer(from, to, amount);
  }

  function _afterTokenTransfer(
    address from,
    address to,
    uint256 fromBalanceBefore,
    uint256 toBalanceBefore,
    uint256 amount
  ) internal virtual override {
    _delegationChangeOnTransfer(
      from,
      to,
      fromBalanceBefore,
      toBalanceBefore,
      amount
    );
  }

  function _getDelegationState(
    address user
  ) internal view override returns (DelegationState memory) {
    DelegationAwareBalance memory userState = _balances[user];
    return
      DelegationState({
        delegatedPropositionBalance: userState.delegatedPropositionBalance,
        delegatedVotingBalance: userState.delegatedVotingBalance,
        delegationMode: userState.delegationMode
      });
  }

  function _getBalance(address user) internal view override returns (uint256) {
    return balanceOf(user);
  }

  function getPowerCurrent(
    address user,
    GovernancePowerType delegationType
  ) public view override returns (uint256) {
    return
      (super.getPowerCurrent(user, delegationType) * EXCHANGE_RATE_UNIT) /
      getExchangeRate();
  }

  function _setDelegationState(
    address user,
    DelegationState memory delegationState
  ) internal override {
    DelegationAwareBalance storage userState = _balances[user];
    userState.delegatedPropositionBalance = delegationState
      .delegatedPropositionBalance;
    userState.delegatedVotingBalance = delegationState.delegatedVotingBalance;
    userState.delegationMode = delegationState.delegationMode;
  }

  function _incrementNonces(address user) internal override returns (uint256) {
    unchecked {
      // Does not make sense to check because it's not realistic to reach uint256.max in nonce
      return _nonces[user]++;
    }
  }

  function _getDomainSeparator() internal view override returns (bytes32) {
    return DOMAIN_SEPARATOR();
  }

  /**
   * @dev stub method to be compatibel with emissions manager
   */
  function totalScaledSupply() external returns (uint256) {
    return totalSupply();
  }
}
