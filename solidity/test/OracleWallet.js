/* global artifacts, contract, it, web3, assert, before */

const HodlOracle = artifacts.require('HodlOracle');
const OracleWallet = artifacts.require('OracleWallet');
const OracleFeeWallet = artifacts.require('OracleFeeWallet');
const BigNumber = require('bignumber.js');
const TestUtils = require('./TestUtils.js');


contract('OracleWallet Test', (accounts) => {
    let oracleWalletInst = null;
    let hodlOracleInst = null;
    let oracleFeeWalletInst = null;
    const oracleOwner = accounts[1];
    const hodlOwner = accounts[2];
    const otherUser = accounts[3];

    before(async () => {
        oracleWalletInst = await OracleWallet.deployed();
        oracleFeeWalletInst = await OracleFeeWallet.deployed();
        hodlOracleInst = await HodlOracle.deployed();
    });

    it('Basic test', async () => {
        console.log(`OracleWallet: ${OracleWallet.address}`);
        console.log(`HodlOracle: ${HodlOracle.address}`);

        await hodlOracleInst.deposit({
            value: 10000,
            from: hodlOwner,
        });

        const myBeforeWalletBalance = BigNumber(
            await web3.eth.getBalance(oracleWalletInst.address),
        );
        await hodlOracleInst.trigger({ from: hodlOwner });
        await oracleFeeWalletInst.payback({ from: oracleOwner });
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
            await web3.eth.getBalance(otherUser),
        );
        await oracleWalletInst.withdraw(
            otherUser,
            { from: oracleOwner },
        );
        const myAfterAccountBalance = BigNumber(
            await web3.eth.getBalance(otherUser),
        );

        assert.equal(
            myBeforeAccountBalance.plus(accumulateWalletBalance).toNumber(),
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
        TestUtils.AssertPass(hodlOracleInst.deposit({
            value: 10000,
            from: hodlOwner,
        }));
        let balance = await oracleFeeWalletInst.getBalance(
            hodlOracleInst.address,
            { from: otherUser },
        );
        assert.equal(
            balance.toNumber(),
            10000,
            'balance should be the same',
        );
        await oracleWalletInst.updateUsedBalance(
            hodlOracleInst.address,
            10000,
            { from: oracleOwner },
        );
        balance = await oracleFeeWalletInst.getBalance(
            hodlOracleInst.address,
            { from: otherUser },
        );
        assert.equal(
            balance.toNumber(),
            0,
            'balance should be the same',
        );
        await oracleFeeWalletInst.payback({ from: oracleOwner });
        balance = await web3.eth.getBalance(oracleWalletInst.address);
        assert.equal(
            balance.toNumber(),
            10000,
            'balance should be the same',
        );
    });
});
