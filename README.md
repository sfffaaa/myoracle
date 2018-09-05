[![Build Status](https://travis-ci.com/sfffaaa/myoracle.svg?branch=master)](https://travis-ci.com/sfffaaa/myoracle)

# Myoracle
Implement an simple oracle which can communicate with the world. One application using my oracle is user allows to save ETH into hodl saver and the same amount of ETH will sent back when ETH price is above threshold user set.

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
### Setup Flow
1. Setup config file.
2. Deploy all smart contract and register related address.
	1. Deploy all smart contract with owner.
	2. Smart contract, oracle register, regists address.
	3. Smart contract, hodl register, regists address.
	4. Smart contract, hodl storage, regists allower.
	5. Smart contract, oracle fee wallet, registers client address.
3. Execute daemon in oracle\_node\_client\_daemon.py.
4. Deposit some eth into HodlOracle by deposit function.
5. Interested user set threshold and transfer ETH to HodlSaver by deposit function.
6. Execute trigger function in HodlOracle smart contract.
If ETH price is above threshold, money will send back to user who deposit ETH in step 5, otherwise, no action will execute.
7. Oracle owner can execute payback function for transfer money all record into oracle fee wallet.
8. Repeat step 6.

### Trigger Flow
1. Execute trigger function in HodlOracle (called by HodlOracle owner).
2. Run \_\_queryNode in OracleBase (called by HodlOracle contract address). </br>
Because \_\_queryNode has permission check, it only allowes HodlOracle owner or HodlOracle itself.
3. Execute querySentNode in OracleCore (called by HodlOracle contract address).
4. Emit ToOracleNode. </br>
Emit ToOracleNode will trigger node to execute request outside. We'll discuss the flow later.
5. Return qureyID back.
### Oracle Node Flow
1. OracleNode execute some requests.
2. Execute function, resultSentBack, in OracleCore (called by OracleCore owner).
3. Run \_\_callback in HodlOracle (called by OracleCore contract address).
### TODO
1. Deposit fee wallet in OracleBase.
2. resultSentBack should change the owner for seperating the setting.
## Payment system
### Flow
1. Users should deposit ETH into oracle fee wallet for paying transaction fee and oracle fee.
2. In functions, trigger and \_\_callback, should check whether the address has enough money in wallet.
3. Before executing real logic in above function, substract the total trasaction fee in wallet and update it.</br>
**Note**: It means I use all trasaction fee instead of real transaction fee.
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
1. Add new smart contract file.
2. Update migration script.
#### Backend
1. Add two file under src/subfolder. For example, folder, oracle\_wallet, has two files, oracle\_wallet.py and oracle\_wallet\_onchain\_handler.py
2. Update src/utils/my\_deployer.py to check how to update.
3. Update contract name to target\_contract\_name in config.conf.template and travisCI/test\_config.conf.
