// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {EthereumScript} from 'aave-helpers/ScriptUtils.sol';
import {UpdateStkAavePayload, ProposalPayloadStkAbpt} from '../src/contracts/ProposalPayload.sol';

contract DeployUpdateStkPayload is EthereumScript {
  address public constant STK_IMPL = address(1);

  function run() external broadcast {
    new UpdateStkAavePayload(STK_IMPL);
  }
}

contract DeployUpdateABPTPayload is EthereumScript {
  function run() external broadcast {
    new ProposalPayloadStkAbpt();
  }
}
