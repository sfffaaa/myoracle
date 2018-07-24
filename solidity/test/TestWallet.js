/* global artifacts, contract, it, web3, assert */

const TestWallet = artifacts.require('TestWallet');
const BigNumber = require('bignumber.js');
const TestUtils = require('./TestUtils.js');


contract('TestWallet Test', (accounts) => {
    it('Basic test', async () => {
        console.log(`TestWallet: ${TestWallet.address}`);

        const testWalletInst = await TestWallet.deployed();

        const myBeforeWalletBalance = BigNumber(
            await web3.eth.getBalance(testWalletInst.address),
        );
        await testWalletInst.deposit({
            value: TestUtils.ALLOW_PAYMENT_VALUE,
            from: accounts[0],
        });
        const myAfterWalletBalance = BigNumber(
            await web3.eth.getBalance(testWalletInst.address),
        );
        assert.equal(
            myBeforeWalletBalance.plus(TestUtils.ALLOW_PAYMENT_VALUE).toNumber(),
            myAfterWalletBalance.toNumber(),
            'balance should be the same',
        );

        let accumulateWalletBalance = BigNumber(
            await web3.eth.getBalance(testWalletInst.address),
        );
        const myBeforeAccountBalance = BigNumber(
            await web3.eth.getBalance(accounts[0]),
        );
        const tx = await testWalletInst.withdraw(accounts[0], {
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
            await web3.eth.getBalance(testWalletInst.address),
        );

        assert.equal(
            accumulateWalletBalance.toNumber(),
            BigNumber(0).toNumber(),
            'Wallet balance should be zero',
        );
    });
});
