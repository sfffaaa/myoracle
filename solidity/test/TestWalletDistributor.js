/* global artifacts, contract, it, web3, assert */

const BigNumber = require('bignumber.js');
const truffleAssert = require('truffle-assertions');

const TestWalletDistributor = artifacts.require('TestWalletDistributor');


contract('TestWalletDistributor Test', (accounts) => {
    it('Basic test', async () => {
        console.log(`TestWalletDistributor: ${TestWalletDistributor.address}`);

        const TestWalletDistributorInst = await TestWalletDistributor.deployed();

        let myBalance = BigNumber(
            await web3.eth.getBalance(TestWalletDistributorInst.address),
        );

        // check tx
        let tx = await TestWalletDistributorInst.depositBalance(100, {
            value: 10000,
            from: accounts[0],
        });
        truffleAssert.eventEmitted(tx, 'DepositBalance', (ev) => {
            assert.equal(ev.myAddress, accounts[0], 'account should be the same');
            assert.equal(ev.threshold.toNumber(), 100, 'threshold should be the same');
            assert.equal(ev.nowValue.toNumber(), 10000, 'now value should be the same');
            assert.equal(
                ev.accuValue.toNumber(),
                myBalance.plus(10000).toNumber(),
                'accumulate value should be the same',
            );
            return true;
        });

        let checkBalance = BigNumber(
            await web3.eth.getBalance(TestWalletDistributorInst.address),
        );
        assert.equal(
            myBalance.plus(10000).toNumber(),
            checkBalance.toNumber(),
            'Should be the same',
        );
        myBalance = checkBalance;

        tx = await TestWalletDistributorInst.depositBalance(200, {
            value: 20000,
            from: accounts[0],
        });
        truffleAssert.eventEmitted(tx, 'DepositBalance', (ev) => {
            assert.equal(ev.myAddress, accounts[0], 'account should be the same');
            assert.equal(ev.threshold.toNumber(), 200, 'threshold should be the same');
            assert.equal(ev.nowValue.toNumber(), 20000, 'now value should be the same');
            assert.equal(
                ev.accuValue.toNumber(),
                myBalance.plus(20000).toNumber(),
                'accumulate value should be the same',
            );
            return true;
        });

        checkBalance = BigNumber(
            await web3.eth.getBalance(TestWalletDistributorInst.address),
        );
        assert.equal(
            myBalance.plus(20000).toNumber(),
            checkBalance.toNumber(),
            'Should be the same',
        );
        myBalance = checkBalance;

        // check tx
        tx = await TestWalletDistributorInst.withdrawBalance(199);
        truffleAssert.eventEmitted(tx, 'WithdrawBalance', (ev) => {
            assert.equal(ev.myAddress, accounts[0], 'address should be the same');
            assert.equal(ev.threshold.toNumber(), 200, 'threshold should be the same');
            assert.equal(ev.price.toNumber(), 199, 'price should be the same');
            assert.equal(ev.transfered, false, 'transfered should be the same');
            return true;
        });
        checkBalance = BigNumber(
            await web3.eth.getBalance(TestWalletDistributorInst.address),
        );
        assert.equal(
            myBalance.toNumber(),
            checkBalance.toNumber(),
            'Should be the same',
        );

        // check tx
        tx = await TestWalletDistributorInst.withdrawBalance(201);
        truffleAssert.eventEmitted(tx, 'WithdrawBalance', (ev) => {
            assert.equal(ev.myAddress, accounts[0], 'address should be the same');
            assert.equal(ev.threshold.toNumber(), 200, 'threshold should be the same');
            assert.equal(ev.price.toNumber(), 201, 'price should be the same');
            assert.equal(ev.transfered, true, 'transfered should be the same');
            return true;
        });

        // check balance on accounts[0]
        checkBalance = BigNumber(
            await web3.eth.getBalance(TestWalletDistributorInst.address),
        );
        assert.equal(
            checkBalance.toNumber(),
            BigNumber(0).toNumber(),
            'Should be the same',
        );
    });
});
