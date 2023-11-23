// SPDX-License-Identifier: agpl-3.0
pragma solidity ^0.8.0;

import 'forge-std/Test.sol';
import {GovHelpers} from 'aave-helpers/GovHelpers.sol';
import {StakedTokenV3} from '../src/contracts/StakedTokenV3.sol';
import {IInitializableAdminUpgradeabilityProxy} from '../src/interfaces/IInitializableAdminUpgradeabilityProxy.sol';
import {BaseTest} from './BaseTest.sol';

contract GhoDistributionGasTest is BaseTest {
  function setUp() public {
    _setUp(true);
  }

  function test_transferWithCorrectGas() public {
    uint256 amount = 10 ether;
    uint256 gasLimit = 300_000 - 13_000;

    address user = address(1234);

    deal(address(STAKE_CONTRACT.STAKED_TOKEN()), user, amount);
    console.log('balance', STAKE_CONTRACT.STAKED_TOKEN().balanceOf(user));

    hoax(user);
    STAKE_CONTRACT.STAKED_TOKEN().approve(
      address(STAKE_CONTRACT),
      type(uint256).max
    );
    console.log(
      'balance',
      STAKE_CONTRACT.STAKED_TOKEN().allowance(user, address(STAKE_CONTRACT))
    );

    hoax(user);
    STAKE_CONTRACT.stake{gas: gasLimit}(user, amount);
  }
}
