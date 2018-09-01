/* global artifacts, contract, it, assert, before */

const OracleFeeWallet = artifacts.require('OracleFeeWallet');
const BigNumber = require('bignumber.js');
const truffleAssert = require('truffle-assertions');
const TestUtils = require('./TestUtils.js');

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

async function CheckUpdateUsedBalanceEvent(
    oracleFeeWalletInst,
    sentValue,
    usedAccountInfo,
    helpAccountInfo,
) {
    const tx = await oracleFeeWalletInst.updateUsedBalance(
        usedAccountInfo.addr,
        sentValue, {
            from: helpAccountInfo.addr,
        },
    );

    truffleAssert.eventEmitted(tx, 'UpdateUsedAction', (ev) => {
        assert.equal(ev.helperInfo, helpAccountInfo.addr, 'Account should be the same');
        assert.equal(ev.balanceAddr, usedAccountInfo.addr, 'Account should be the same');
        assert.equal(
            ev.value.toNumber(),
            BigNumber(usedAccountInfo.sentValue).toNumber(),
            'Value should be the same',
        );
        assert.equal(
            ev.accumulateValue.toNumber(),
            BigNumber(usedAccountInfo.accumulateValue).toNumber(),
            'Accumulate Value should be the same',
        );
        return true;
    });

    truffleAssert.eventEmitted(tx, 'UpdatePaybackAction', (ev) => {
        assert.equal(ev.helperAddr, helpAccountInfo.addr, 'Account should be the same');
        assert.equal(ev.balanceAddr, usedAccountInfo.addr, 'Account should be the same');
        assert.equal(
            ev.value.toNumber(),
            BigNumber(sentValue.sentValue).toNumber(),
            'Value should be the same',
        );
        assert.equal(
            ev.accumulateValue.toNumber(),
            BigNumber(helpAccountInfo.accumulateValue).toNumber(),
            'Accumulate Value should be the same',
        );
        return true;
    });
}

function UpdateUsedBalance(sentValue, usedAccountInfo, helpAccountInfo) {
    assert.isAtLeast(
        usedAccountInfo.accumulateValue,
        sentValue,
        'value should larger than usedAccountInfo.accumulateValue',
    );
    const newUsedAccountInfo = usedAccountInfo;
    const newHelpAccountInfo = helpAccountInfo;
    newUsedAccountInfo.accumulateValue -= sentValue;
    newHelpAccountInfo.accumulateValue += sentValue;
    return {
        usedInfo: newUsedAccountInfo,
        helperInfo: newHelpAccountInfo,
    };
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

    it('Update check test', async () => {
        await oracleFeeWalletInst.deposit({
            from: accounts[1],
            value: 1000,
        });
        await oracleFeeWalletInst.deposit({
            from: accounts[2],
            value: 2000,
        });
        const helperInfos = [{
            addr: accounts[3],
            accumulateValue: 0,
        }, {
            addr: accounts[4],
            accumulateValue: 0,
        }];

        const usedInfos = [{
            addr: accounts[1],
            accumulateValue: (await oracleFeeWalletInst.getBalance.call(accounts[1])).toNumber(),
        }, {
            addr: accounts[2],
            accumulateValue: (await oracleFeeWalletInst.getBalance.call(accounts[2])).toNumber(),
        }];

        // use account1 and update in account3
        let sentValue = 100;
        let afterInfoDict = UpdateUsedBalance(sentValue, usedInfos[0], helperInfos[0]);
        usedInfos[0] = afterInfoDict.usedInfo;
        helperInfos[0] = afterInfoDict.helperInfo;
        CheckUpdateUsedBalanceEvent(
            oracleFeeWalletInst,
            sentValue,
            usedInfos[0],
            helperInfos[0],
        );

        // use account1 and update in account3
        sentValue = 200;
        afterInfoDict = UpdateUsedBalance(sentValue, usedInfos[0], helperInfos[0]);
        usedInfos[0] = afterInfoDict.usedInfo;
        helperInfos[0] = afterInfoDict.helperInfo;
        CheckUpdateUsedBalanceEvent(
            oracleFeeWalletInst,
            sentValue,
            usedInfos[0],
            helperInfos[0],
        );

        // use account2 and update in account3
        sentValue = 300;
        afterInfoDict = UpdateUsedBalance(sentValue, usedInfos[1], helperInfos[0]);
        usedInfos[1] = afterInfoDict.usedInfo;
        helperInfos[0] = afterInfoDict.helperInfo;
        CheckUpdateUsedBalanceEvent(
            oracleFeeWalletInst,
            sentValue,
            usedInfos[1],
            helperInfos[0],
        );

        // use account2 and update in account4
        sentValue = 400;
        afterInfoDict = UpdateUsedBalance(sentValue, usedInfos[1], helperInfos[1]);
        usedInfos[1] = afterInfoDict.usedInfo;
        helperInfos[1] = afterInfoDict.helperInfo;
        CheckUpdateUsedBalanceEvent(
            oracleFeeWalletInst,
            sentValue,
            usedInfos[1],
            helperInfos[1],
        );
        TestUtils.AssertRevert(oracleFeeWalletInst.updateUsedBalance(
            accounts[8],
            1000000000, {
                from: accounts[3],
            },
        ));
    });
});
