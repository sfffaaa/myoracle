[![Build Status](https://travis-ci.org/sfffaaa/myoracle.svg?branch=issue_2)](https://travis-ci.org/sfffaaa/myoracle)

# Myoracle
Implement an simple oracle which can communicate with the world

# Deploy
## Smart contract
```bash
cd solidity
npm install
```
## Backend
```bash
cd backend
pip3 install -r requirements.txt
```

# Design Note
## Flow
### Trigger Flow
1. trigger in TestOracleExample (called by TestOracleExample owner)
2. \_\_queryNode in OracleBase (called by TestOracleExample contract address) </br>
Because \_\_queryNode has permission check, it only allowes TestOracleExample owner or TestOracleExample itself.
3. querySentNode in OracleCore (called by TestOracleExample contract address)
4. emit ToOracleNode </br>
Emit ToOracleNode will trigger node to execute request outside. We'll discuss the flow later.
5. return qureyID
### Oracle Node Flow
1. OracleNode execute some requests
2. resultSentBack in OracleCore (called by OracleCore owner)
3. \_\_callback in TestOracleExample (called by OracleCore contract address)
### TODO
1. Deposit fee wallet in OracleBase
2. resultSentBack should change the owner for seperating the setting
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
## Q&A
### How to create your oracle related contract
### How to run your oracle node
### How to Add new smart contract
#### Solidity
1. Add new smart contract file
2. Update migration script
#### Backend
1. Add two file under src/subfolder. For example, folder, oracle\_wallet, has two files, oracle\_wallet.py and oracle\_wallet\_onchain\_handler.py
2. Update src/utils/my\_deployer.py to check how to update.
3. Update contract name to target\_contract\_name in config.conf.template and travisCI/test\_config.conf.
