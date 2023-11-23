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
import {IERC20Metadata} from 'openzeppelin-contracts/contracts/token/ERC20/extensions/IERC20Metadata.sol';

contract GhoDistributionGasTest is Test, StakedAaveV3 {
  address ghoToken = 0x786dBff3f1292ae8F92ea68Cf93c30b34B1ed04B; //0x40D16FC0246aD3160Ccc09B8D0D3A2cD28aE6C2f;

  function setUp() public {
    vm.createSelectFork(vm.rpcUrl('mainnet'), 18636130);
    console.log(
      IERC20Metadata(address(AaveV3EthereumAssets.AAVE_UNDERLYING)).decimals()
    );
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
    uint256 gasLimit = 4_000;

    address from = 0xE831C8903de820137c13681E78A5780afDdf7697;
    address to = address(123415);
    uint256 fromBalance = 10 ether;
    uint256 toBalance = 0 ether;

    uint256 amount = 1 ether;

    vm.expectRevert();
    this.updateDiscountDistribution{gas: gasLimit}(
      ghoToken,
      from,
      to,
      fromBalance,
      toBalance,
      amount
    );

    // expect error but not revert
    this.updateDiscountDistribution(
      ghoToken,
      from,
      to,
      fromBalance,
      toBalance,
      amount
    );
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
