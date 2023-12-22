import {ZeroAddress, JsonRpcProvider, Interface, id, zeroPadBytes} from 'ethers';
import {getLogs} from './eventLogs';
import fs from 'fs';

import dotenv from 'dotenv';
dotenv.config();

export const roleGrantedEventABI = [
  'event Transfer(address indexed from, address indexed to, uint256 value)',
];

export const ercABI = ['function balanceOf(address) external returns (uint256)'];

export const parseLog = (abi: string[], eventLog: any): {from: string; to: string} => {
  const iface = new Interface(abi);
  const parsedEvent = iface.parseLog(eventLog);
  // @ts-ignore
  const {from, to} = parsedEvent.args;

  return {from, to};
};

const getHolders = async () => {
  const stkToken = '0x4da27a545c0c5B758a6BA100e3a049001de870f5';

  const provider = new JsonRpcProvider(process.env.RPC_MAINNET);

  const topic0 = id('Transfer(address,address,uint256)');

  // get burn events
  const topic2 = zeroPadBytes(ZeroAddress, 32);
  const burnLogs = await getLogs({
    provider,
    address: stkToken,
    fromBlock: 10927018,
    maxBlock: 18841250,
    logs: [],
    topic0,
    topic2,
  });

  console.log('length burn: ', burnLogs.eventLogs.length);

  const burners = new Set<string>();
  for (let i = 0; i < burnLogs.eventLogs.length; i++) {
    const {to} = parseLog(roleGrantedEventABI, burnLogs.eventLogs[i]);
    burners.add(to);
  }

  const topic1 = zeroPadBytes(ZeroAddress, 32);
  console.log(topic1);
  const mintLogs = await getLogs({
    provider,
    address: stkToken,
    fromBlock: 10927018,
    maxBlock: 18841250,
    logs: [],
    topic0,
    topic1,
  });

  console.log('length mint: ', mintLogs.eventLogs.length);

  const holders = new Set<string>();
  for (let i = 0; i < mintLogs.eventLogs.length; i++) {
    const {to} = parseLog(roleGrantedEventABI, mintLogs.eventLogs[i]);
    if (!burners.has(to)) {
      holders.add(to);
    }
  }

  console.log('holders: ', holders.size);

  const object = {
    holders: [...holders].slice(0, 100),
  };

  const higherBalanceHolders = [
    '0x9bec07CB8E702FA848Cda6A958453455053a016e',
    '0xF23c8539069C471F5C12692a3471C9F4E8B88BC2',
    '0xE466d6Cf6E2C3F3f8345d39633d4A968EC879bD5',
    '0xe705b1D26B85c9F9f91A3690079D336295F14F08',
    '0xaFDAbFb6227507fF6522b8a242168F6b5F353a6E',
    '0xc4a936B003BC223DF757B35Ee52f6Da66B062935',
  ];

  object.holders = [...higherBalanceHolders, ...object.holders];

  fs.writeFileSync('./tests/utils/stkHolders.json', JSON.stringify(object));
};

getHolders().then().catch();
