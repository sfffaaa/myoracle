/* global artifacts, contract, it, web3, assert, before */

const TestOracleExample = artifacts.require('TestOracleExample');
const OracleWallet = artifacts.require('OracleWallet');
const OracleFeeWallet = artifacts.require('OracleFeeWallet');
const BigNumber = require('bignumber.js');
const TestUtils = require('./TestUtils.js');


contract('OracleWallet Test', (accounts) => {
    let oracleWalletInst = null;
    let testOracleExampleInst = null;
    let oracleFeeWalletInst = null;

    before(async () => {
        oracleWalletInst = await OracleWallet.deployed();
        oracleFeeWalletInst = await OracleFeeWallet.deployed();
        testOracleExampleInst = await TestOracleExample.deployed();
    });

    it('Basic test', async () => {
        console.log(`OracleWallet: ${OracleWallet.address}`);
        console.log(`TestOracleExample: ${TestOracleExample.address}`);

        TestUtils.AssertPass(testOracleExampleInst.deposit({
            value: 10000,
        }));

        const myBeforeWalletBalance = BigNumber(
            await web3.eth.getBalance(oracleWalletInst.address),
        );
        await testOracleExampleInst.trigger(
            {
                from: accounts[0],
            },
        );
        await oracleFeeWalletInst.payback({ from: accounts[0] });
        const myAfterWalletBalance = BigNumber(
            await web3.eth.getBalance(oracleWalletInst.address),
        );
        assert.equal(
            myBeforeWalletBalance.plus(10000).toNumber(),
            myAfterWalletBalance.toNumber(),
            'balance should be the same',
        );

        let accumulateWalletBalance = BigNumber(
            await web3.eth.getBalance(oracleWalletInst.address),
        );
        const myBeforeAccountBalance = BigNumber(
            await web3.eth.getBalance(accounts[0]),
        );
        const tx = await oracleWalletInst.withdraw(accounts[0], {
            from: accounts[0],
        });
        const myAfterAccountBalance = BigNumber(
            await web3.eth.getBalance(accounts[0]),
        );
        const txDetail = await web3.eth.getTransaction(tx.tx);
        const realGasUsed = txDetail.gasPrice.mul(tx.receipt.gasUsed);

        assert.equal(
            myBeforeAccountBalance.minus(realGasUsed).plus(accumulateWalletBalance).toNumber(),
            myAfterAccountBalance.toNumber(),
            'balance should be the same',
        );

        accumulateWalletBalance = BigNumber(
            await web3.eth.getBalance(oracleWalletInst.address),
        );

        assert.equal(
            accumulateWalletBalance.toNumber(),
            BigNumber(0).toNumber(),
            'Wallet balance should be zero',
        );
    });

    it('Update check test', async () => {

        TestUtils.AssertPass(testOracleExampleInst.deposit({
            value: 10000,
        }));
        assert.equal(
            (await oracleFeeWalletInst.getBalance(testOracleExampleInst.address)).toNumber(),
            10000,
            'balance should be the same',
        );
        await oracleWalletInst.updateUsedBalance(testOracleExampleInst.address, 10000, {
            from: accounts[0],
        });
        assert.equal(
            (await oracleFeeWalletInst.getBalance(testOracleExampleInst.address)).toNumber(),
            0,
            'balance should be the same',
        );
        await oracleFeeWalletInst.payback();
        assert.equal(
            (await web3.eth.getBalance(oracleWalletInst.address).toNumber()),
            10000,
            'balance should be the same',
        );
    });
});
