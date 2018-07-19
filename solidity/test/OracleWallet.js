/* global artifacts, contract, it, web3, assert */

const TestOracleExample = artifacts.require('TestOracleExample');
const OracleWallet = artifacts.require('OracleWallet');
const BigNumber = require('bignumber.js');
const TestUtils = require('./TestUtils.js');


contract('OracleWallet Test', (accounts) => {
    it('Basic test', async () => {
        console.log(`OracleWallet: ${OracleWallet.address}`);
        console.log(`TestOracleExample: ${TestOracleExample.address}`);

        const oracleWalletInst = await OracleWallet.deployed();
        const testOracleExampleInst = await TestOracleExample.deployed();

        const myBeforeWalletBalance = BigNumber(
            await web3.eth.getBalance(oracleWalletInst.address),
        );
        await testOracleExampleInst.trigger(
            {
                value: TestUtils.ALLOW_PAYMENT_VALUE,
                from: accounts[0],
            },
        );
        const myAfterWalletBalance = BigNumber(
            await web3.eth.getBalance(oracleWalletInst.address),
        );
        assert.equal(
            myBeforeWalletBalance.plus(TestUtils.ALLOW_PAYMENT_VALUE).toNumber(),
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
});
