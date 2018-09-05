/* global artifacts, contract, it, web3, assert, before */

const BigNumber = require('bignumber.js');
const truffleAssert = require('truffle-assertions');

const HodlSaver = artifacts.require('HodlSaver');
const TestUtils = require('./TestUtils.js');


contract('HodlSaver Test', (accounts) => {
    let hodlSaverInst = null;
    const hodlOwner = accounts[2];
    const otherUserA = accounts[3];
    const otherUserB = accounts[4];

    before(async () => {
        console.log(`HodlSaver: ${HodlSaver.address}`);
        hodlSaverInst = await HodlSaver.deployed();
    });

    it('Basic test', async () => {
        let myBalance = BigNumber(
            await web3.eth.getBalance(hodlSaverInst.address),
        );

        // check tx
        let tx = await hodlSaverInst.depositBalance(100, {
            value: 10000,
            from: otherUserA,
        });
        truffleAssert.eventEmitted(tx, 'DepositBalance', (ev) => {
            assert.equal(ev.myAddress, otherUserA, 'account should be the same');
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
            await web3.eth.getBalance(hodlSaverInst.address),
        );
        assert.equal(
            myBalance.plus(10000).toNumber(),
            checkBalance.toNumber(),
            'Should be the same',
        );
        myBalance = checkBalance;

        tx = await hodlSaverInst.depositBalance(200, {
            value: 20000,
            from: otherUserA,
        });
        truffleAssert.eventEmitted(tx, 'DepositBalance', (ev) => {
            assert.equal(ev.myAddress, otherUserA, 'account should be the same');
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
            await web3.eth.getBalance(hodlSaverInst.address),
        );
        assert.equal(
            myBalance.plus(20000).toNumber(),
            checkBalance.toNumber(),
            'Should be the same',
        );
        myBalance = checkBalance;

        // check tx
        tx = await hodlSaverInst.withdrawBalance(
            199,
            { from: hodlOwner },
        );
        truffleAssert.eventEmitted(tx, 'WithdrawBalance', (ev) => {
            assert.equal(ev.myAddress, otherUserA, 'address should be the same');
            assert.equal(ev.threshold.toNumber(), 200, 'threshold should be the same');
            assert.equal(ev.price.toNumber(), 199, 'price should be the same');
            assert.equal(ev.transfered, false, 'transfered should be the same');
            return true;
        });
        checkBalance = BigNumber(
            await web3.eth.getBalance(hodlSaverInst.address),
        );
        assert.equal(
            myBalance.toNumber(),
            checkBalance.toNumber(),
            'Should be the same',
        );

        // check tx
        tx = await hodlSaverInst.withdrawBalance(
            201,
            { from: hodlOwner },
        );
        truffleAssert.eventEmitted(tx, 'WithdrawBalance', (ev) => {
            assert.equal(ev.myAddress, otherUserA, 'address should be the same');
            assert.equal(ev.threshold.toNumber(), 200, 'threshold should be the same');
            assert.equal(ev.price.toNumber(), 201, 'price should be the same');
            assert.equal(ev.transfered, true, 'transfered should be the same');
            return true;
        });

        // check balance on accounts[0]
        checkBalance = BigNumber(
            await web3.eth.getBalance(hodlSaverInst.address),
        );
        assert.equal(
            checkBalance.toNumber(),
            BigNumber(0).toNumber(),
            'Should be the same',
        );
    });

    it('Two user test', async () => {
        const depositValues = [10000, 20000];
        const thresholdValues = [100, 200];
        const testPrices = [50, 150, 250];

        let myBalance = BigNumber(
            await web3.eth.getBalance(hodlSaverInst.address),
        );

        // check tx
        let tx = await hodlSaverInst.depositBalance(thresholdValues[0], {
            value: depositValues[0],
            from: otherUserA,
        });
        truffleAssert.eventEmitted(tx, 'DepositBalance', (ev) => {
            assert.equal(ev.myAddress, otherUserA, 'account should be the same');
            assert.equal(ev.threshold.toNumber(), thresholdValues[0], 'threshold should be the same');
            assert.equal(ev.nowValue.toNumber(), depositValues[0], 'now value should be the same');
            assert.equal(
                ev.accuValue.toNumber(),
                BigNumber(depositValues[0]).toNumber(),
                'accumulate value should be the same',
            );
            return true;
        });

        let checkBalance = BigNumber(
            await web3.eth.getBalance(hodlSaverInst.address),
        );
        assert.equal(
            myBalance.plus(depositValues[0]).toNumber(),
            checkBalance.toNumber(),
            'Should be the same',
        );
        myBalance = checkBalance;

        tx = await hodlSaverInst.depositBalance(thresholdValues[1], {
            value: depositValues[1],
            from: otherUserB,
        });
        truffleAssert.eventEmitted(tx, 'DepositBalance', (ev) => {
            assert.equal(ev.myAddress, otherUserB, 'account should be the same');
            assert.equal(ev.threshold.toNumber(), thresholdValues[1], 'threshold should be the same');
            assert.equal(ev.nowValue.toNumber(), depositValues[1], 'now value should be the same');
            assert.equal(
                ev.accuValue.toNumber(),
                BigNumber(depositValues[1]).toNumber(),
                'accumulate value should be the same',
            );
            return true;
        });

        checkBalance = BigNumber(
            await web3.eth.getBalance(hodlSaverInst.address),
        );
        assert.equal(
            myBalance.plus(depositValues[1]).toNumber(),
            checkBalance.toNumber(),
            'Should be the same',
        );
        myBalance = checkBalance;

        let myIdx = 0;

        // check tx (no user withdraw)
        tx = await hodlSaverInst.withdrawBalance(
            testPrices[0],
            { from: hodlOwner },
        );
        truffleAssert.eventEmitted(tx, 'WithdrawBalance', (ev) => {
            if (myIdx === 0) {
                assert.equal(ev.myAddress, otherUserA, 'address should be the same');
                assert.equal(ev.threshold.toNumber(), thresholdValues[0], 'threshold should be the same');
                assert.equal(ev.price.toNumber(), testPrices[0], 'price should be the same');
                assert.equal(ev.transfered, false, 'transfered should be the same');
                myIdx += 1;
            } else {
                assert.equal(ev.myAddress, otherUserB, 'address should be the same');
                assert.equal(ev.threshold.toNumber(), thresholdValues[1], 'threshold should be the same');
                assert.equal(ev.price.toNumber(), testPrices[0], 'price should be the same');
                assert.equal(ev.transfered, false, 'transfered should be the same');
                myIdx += 1;
            }
            return true;
        });
        checkBalance = BigNumber(
            await web3.eth.getBalance(hodlSaverInst.address),
        );
        assert.equal(
            myBalance.toNumber(),
            checkBalance.toNumber(),
            'Should be the same',
        );
        myBalance = checkBalance;
        myIdx = 0;

        // check tx (one of users withdraw)
        tx = await hodlSaverInst.withdrawBalance(
            testPrices[1],
            { from: hodlOwner },
        );
        truffleAssert.eventEmitted(tx, 'WithdrawBalance', (ev) => {
            if (myIdx === 0) {
                assert.equal(ev.myAddress, otherUserA, 'address should be the same');
                assert.equal(ev.threshold.toNumber(), thresholdValues[0], 'threshold should be the same');
                assert.equal(ev.price.toNumber(), testPrices[1], 'price should be the same');
                assert.equal(ev.transfered, true, 'transfered should be the same');
                myIdx += 1;
            } else {
                assert.equal(ev.myAddress, otherUserB, 'address should be the same');
                assert.equal(ev.threshold.toNumber(), thresholdValues[1], 'threshold should be the same');
                assert.equal(ev.price.toNumber(), testPrices[1], 'price should be the same');
                assert.equal(ev.transfered, false, 'transfered should be the same');
                myIdx += 1;
            }
            return true;
        });
        checkBalance = BigNumber(
            await web3.eth.getBalance(hodlSaverInst.address),
        );
        assert.equal(
            myBalance.toNumber(),
            checkBalance.plus(depositValues[0]).toNumber(),
            'Should be the same',
        );
        myBalance = checkBalance;
        myIdx = 0;

        // check tx (one of users withdraw)
        tx = await hodlSaverInst.withdrawBalance(
            testPrices[2],
            { from: hodlOwner },
        );
        truffleAssert.eventEmitted(tx, 'WithdrawBalance', (ev) => {
            if (myIdx === 0) {
                assert.equal(ev.myAddress, otherUserA, 'address should be the same');
                assert.equal(ev.threshold.toNumber(), thresholdValues[0], 'threshold should be the same');
                assert.equal(ev.price.toNumber(), testPrices[2], 'price should be the same');
                assert.equal(ev.transfered, false, 'transfered should be the same');
                myIdx += 1;
            } else {
                assert.equal(ev.myAddress, otherUserB, 'address should be the same');
                assert.equal(ev.threshold.toNumber(), thresholdValues[1], 'threshold should be the same');
                assert.equal(ev.price.toNumber(), testPrices[2], 'price should be the same');
                assert.equal(ev.transfered, true, 'transfered should be the same');
                myIdx += 1;
            }
            return true;
        });

        // check balance on accounts[0]
        checkBalance = BigNumber(
            await web3.eth.getBalance(hodlSaverInst.address),
        );
        assert.equal(
            checkBalance.toNumber(),
            BigNumber(0).toNumber(),
            'Should be the same',
        );
    });
    it('Permission test', async () => {
        TestUtils.AssertRevert(hodlSaverInst.withdrawBalance(0, {
            from: otherUserA,
        }));
    });
});
