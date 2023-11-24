// SPDX-License-Identifier: agpl-3.0
pragma solidity ^0.8.0;

import 'forge-std/Test.sol';
import {AaveMisc} from 'aave-address-book/AaveMisc.sol';
import {GovHelpers, AaveGovernanceV2} from 'aave-helpers/GovHelpers.sol';
import {ProxyHelpers} from 'aave-helpers/ProxyHelpers.sol';
import {StakedTokenV3} from '../src/contracts/StakedTokenV3.sol';
import {IInitializableAdminUpgradeabilityProxy} from '../src/interfaces/IInitializableAdminUpgradeabilityProxy.sol';
import {ProxyAdmin, TransparentUpgradeableProxy} from 'openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol';

contract BaseTest is Test {
  StakedTokenV3 STAKE_CONTRACT;

  uint256 constant SLASHING_ADMIN = 0;
  uint256 constant COOLDOWN_ADMIN = 1;
  uint256 constant CLAIM_HELPER_ROLE = 2;

  address slashingAdmin;
  address cooldownAdmin;
  address claimHelper;

  function _setUp() internal {
    StakedTokenV3 token = new StakedTokenV3();
    STAKE_CONTRACT = new StakedTokenV3(token);

    slashingAdmin = STAKE_CONTRACT.getAdmin(SLASHING_ADMIN);
    cooldownAdmin = STAKE_CONTRACT.getAdmin(COOLDOWN_ADMIN);
    claimHelper = STAKE_CONTRACT.getAdmin(CLAIM_HELPER_ROLE);
  }

  function _stake(uint256 amount) internal {
    _stake(amount, address(this));
  }

  function _stake(uint256 amount, address user) internal {
    deal(address(STAKE_CONTRACT.STAKED_TOKEN()), user, amount);
    STAKE_CONTRACT.STAKED_TOKEN().approve(
      address(STAKE_CONTRACT),
      type(uint256).max
    );
    STAKE_CONTRACT.stake(user, amount);
  }

  function _redeem(uint256 amount) internal {
    STAKE_CONTRACT.redeem(address(this), amount);
    assertEq(STAKE_CONTRACT.STAKED_TOKEN().balanceOf(address(this)), amount);
  }

  function _slash20() internal {
    address receiver = address(42);
    uint256 amountToSlash = (STAKE_CONTRACT.previewRedeem(
      STAKE_CONTRACT.totalSupply()
    ) * 2) / 10;

    // slash
    vm.startPrank(STAKE_CONTRACT.getAdmin(SLASHING_ADMIN));
    STAKE_CONTRACT.slash(receiver, amountToSlash);
    vm.stopPrank();
  }

  function _settleSlashing() internal {
    vm.startPrank(slashingAdmin);
    STAKE_CONTRACT.settleSlashing();
    vm.stopPrank();
  }
}
