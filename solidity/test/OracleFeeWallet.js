/* global artifacts, contract, it, assert, before */

const OracleFeeWallet = artifacts.require('OracleFeeWallet');
const BigNumber = require('bignumber.js');
const truffleAssert = require('truffle-assertions');


async function CheckDepositEvent(oracleFeeWalletInst, account, sentValue, accumulateValue) {
    const tx = await oracleFeeWalletInst.deposit({
        from: account,
        value: sentValue,
    });
    truffleAssert.eventEmitted(tx, 'DepositAction', (ev) => {
        assert.equal(ev.sender, account, 'Account should be the same');
        assert.equal(ev.value.toNumber(), BigNumber(sentValue).toNumber(), 'Value should be the same');
        assert.equal(
            ev.accumulateValue.toNumber(),
            BigNumber(accumulateValue).toNumber(),
            'Accumulate Value should be the same',
        );
        return true;
    });
}

contract('OracleFeeWallet Test', (accounts) => {
    let oracleFeeWalletInst = null;

    before(async () => {
        oracleFeeWalletInst = await OracleFeeWallet.deployed();
    });

    it('Deposit test', async () => {
        console.log(`OracleFeeWallet: ${OracleFeeWallet.address}`);

        CheckDepositEvent(oracleFeeWalletInst, accounts[1], 5000, 5000);
        CheckDepositEvent(oracleFeeWalletInst, accounts[2], 10000, 10000);
        CheckDepositEvent(oracleFeeWalletInst, accounts[1], 7000, 12000);
    });

    it('Check balance test', async () => {
        let balance = await oracleFeeWalletInst.getBalance.call(accounts[9]);
        assert.equal(BigNumber(0).toNumber(), balance.toNumber());
        await oracleFeeWalletInst.deposit({
            from: accounts[9],
            value: 1000,
        });
        balance = await oracleFeeWalletInst.getBalance.call(accounts[9]);
        assert.equal(BigNumber(1000).toNumber(), balance.toNumber());
    });
});
