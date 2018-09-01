[![Build Status](https://travis-ci.org/sfffaaa/myoracle.svg?branch=master)](https://travis-ci.org/sfffaaa/myoracle)

# Myoracle
Implement an simple oracle which can communicate with the world

# Smart contract
```bash
npm install
```

# Design Note

## Smart Contract
### Add new smart contract
#### Smart Contract
1. Add new smart contract file
2. Update migration script

#### Backend
1. Add two file under src/subfolder. For example, folder, oracle\_wallet, has two files, oracle\_wallet.py and oracle\_wallet\_onchain\_handler.py
2. Update src/utils/my\_deployer.py to check how to update.
3. Update contract name to target\_contract\_name in config.conf.template and travisCI/test\_config.conf.

## Payment system
### Flow
1. Users should deposit ETH into wallet for paying transaction fee and oracle fee.
2. In functions, trigger and \_\_callback, should check whether the address has enough money in wallet.
3. Before executing real logic in above function, substract the total trasaction fee in wallet and update it.</br>
**Note**: It means I use estimate trasaction fee instead of real transaction fee.
4. Smart contract should emit event for recording all information.

### Wait to Check
1. I want other people can also take responsibility for running node client. So maybe they need to stake some money inside the wallet in order to avoid some illegal activities. And before the money in wallet exceeds client's staking, I should pay back ETH in wallet to other clients where they help to call oracle. </br> It implies below things.
    - The function which pay back to all clients is needed.
    - All receipts need to be recorded for sent back money.
