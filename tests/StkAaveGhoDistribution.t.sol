// SPDX-License-Identifier: agpl-3.0
pragma solidity ^0.8.0;

import 'forge-std/Test.sol';
import {GovHelpers} from 'aave-helpers/GovHelpers.sol';
import {StakedTokenV3} from '../src/contracts/StakedTokenV3.sol';
import {IInitializableAdminUpgradeabilityProxy} from '../src/interfaces/IInitializableAdminUpgradeabilityProxy.sol';
import {BaseTest} from './BaseTest.sol';
import {StakedAaveV3} from '../src/contracts/StakedAaveV3.sol';
import {IERC20} from 'openzeppelin-contracts/contracts/token/ERC20/IERC20.sol';
import {GovernanceV3Ethereum} from 'aave-address-book/GovernanceV3Ethereum.sol';
import {AaveMisc} from 'aave-address-book/AaveMisc.sol';
import {AaveV3EthereumAssets} from 'aave-address-book/AaveV3Ethereum.sol';
import {IGhoVariableDebtTokenTransferHook} from '../src/interfaces/IGhoVariableDebtTokenTransferHook.sol';

contract GhoDistributionGasTest is Test, StakedAaveV3 {
  address ghoToken = 0x40D16FC0246aD3160Ccc09B8D0D3A2cD28aE6C2f;

  function setUp() public {
    vm.createSelectFork(vm.rpcUrl('mainnet'), 18635596);
  }

  constructor()
    StakedAaveV3(
      IERC20(AaveV3EthereumAssets.AAVE_UNDERLYING),
      IERC20(AaveV3EthereumAssets.AAVE_UNDERLYING),
      172800,
      AaveMisc.ECOSYSTEM_RESERVE,
      GovernanceV3Ethereum.EXECUTOR_LVL_1,
      3155692600
    )
  {
    ghoDebtToken = IGhoVariableDebtTokenTransferHook(ghoToken);
  }

  function test_transferWithCorrectGas() public {
    uint256 gasLimit = 300_000 - 64_000;

    address from = address(1234);
    address to = address(123415);
    uint256 fromBalance = 10 ether;
    uint256 toBalance = 10 ether;

    uint256 amount = 1 ether;

    this.updateDiscountDistribution{gas: gasLimit}(
      ghoToken,
      from,
      to,
      fromBalance,
      toBalance,
      amount
    );
    //    address user = address(1234);
    //
    //    deal(address(STAKE_CONTRACT.STAKED_TOKEN()), user, amount);
    //    console.log('balance', STAKE_CONTRACT.STAKED_TOKEN().balanceOf(user));
    //
    //    vm.startPrank(user);
    //    STAKE_CONTRACT.STAKED_TOKEN().approve(
    //      address(STAKE_CONTRACT),
    //      type(uint256).max
    //    );
    //    console.log(
    //      'balance',
    //      STAKE_CONTRACT.STAKED_TOKEN().allowance(user, address(STAKE_CONTRACT))
    //    );
    //
    //    STAKE_CONTRACT.stake{gas: gasLimit}(user, amount);
    //    vm.stopPrank();
  }

  function updateDiscountDistribution(
    address cachedGhoDebtToken,
    address from,
    address to,
    uint256 fromBalanceBefore,
    uint256 toBalanceBefore,
    uint256 amount
  ) external {
    _updateDiscountDistribution(
      cachedGhoDebtToken,
      from,
      to,
      fromBalanceBefore,
      toBalanceBefore,
      amount
    );
  }
}
