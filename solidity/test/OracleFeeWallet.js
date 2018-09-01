/* global artifacts, contract, it, assert */

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
        assert.equal(ev.value, BigNumber(sentValue), 'Value should be the same');
        assert.equal(
            ev.accumulateValue,
            BigNumber(accumulateValue),
            'Accumulate Value should be the same',
        );
        return true;
    });
}

contract('OracleFeeWallet Test', (accounts) => {
    it('Deposit test', async () => {
        console.log(`OracleFeeWallet: ${OracleFeeWallet.address}`);

        const oracleFeeWalletInst = await OracleFeeWallet.deployed();

        CheckDepositEvent(oracleFeeWalletInst, accounts[1], 5000, 5000);
        CheckDepositEvent(oracleFeeWalletInst, accounts[2], 10000, 10000);
        CheckDepositEvent(oracleFeeWalletInst, accounts[1], 7000, 12000);
    });
});
