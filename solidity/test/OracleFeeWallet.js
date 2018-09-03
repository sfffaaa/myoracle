/* global artifacts, contract, it, assert, before, web3 */

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
        sentValue.toNumber(), {
            from: helpAccountInfo.addr,
        },
    );

    truffleAssert.eventEmitted(tx, 'UpdateUsedAction', (ev) => {
        assert.equal(ev.helperAddr, helpAccountInfo.addr, 'Account should be the same');
        assert.equal(ev.balanceAddr, usedAccountInfo.addr, 'Account should be the same');
        assert.equal(
            ev.value.toNumber(),
            sentValue.toNumber(),
            'Value should be the same',
        );
        assert.equal(
            ev.accumulateValue.toNumber(),
            usedAccountInfo.accumulateValue.toNumber(),
            'Accumulate Value should be the same',
        );
        return true;
    });

    truffleAssert.eventEmitted(tx, 'UpdatePaybackAction', (ev) => {
        assert.equal(ev.helperAddr, helpAccountInfo.addr, 'Account should be the same');
        assert.equal(ev.balanceAddr, usedAccountInfo.addr, 'Account should be the same');
        assert.equal(
            ev.value.toNumber(),
            sentValue.toNumber(),
            'Value should be the same',
        );
        assert.equal(
            ev.accumulateValue.toNumber(),
            helpAccountInfo.accumulateValue.toNumber(),
            'Accumulate Value should be the same',
        );
        return true;
    });
}

async function CheckPaybackEvent(
    oracleFeeWalletInst,
    paybackInfos,
    account,
) {
    const tx = await oracleFeeWalletInst.payback({
        from: account,
    });
    let myIdx = 0;
    truffleAssert.eventEmitted(tx, 'PaybackAction', (ev) => {
        const testEvent = ev;
        const checkInfo = paybackInfos[myIdx];
        assert.equal(testEvent.paybackAddr, checkInfo.addr, 'address should be the same');
        assert.equal(
            testEvent.paybackValue.toNumber(),
            checkInfo.accumulateValue.toNumber(),
            'payback value should be the same',
        );
        myIdx += 1;
        return true;
    });
    assert.equal(myIdx, paybackInfos.length, 'length should be the same');
}

function UpdateUsedBalance(sentValue, usedAccountInfo, helpAccountInfo) {
    assert.isAtLeast(
        usedAccountInfo.accumulateValue.toNumber(),
        sentValue.toNumber(),
        'value should larger than usedAccountInfo.accumulateValue',
    );
    const newUsedAccountInfo = usedAccountInfo;
    const newHelpAccountInfo = helpAccountInfo;
    newUsedAccountInfo.accumulateValue = newUsedAccountInfo.accumulateValue.minus(sentValue);
    newHelpAccountInfo.accumulateValue = newHelpAccountInfo.accumulateValue.plus(sentValue);
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

        await CheckDepositEvent(oracleFeeWalletInst, accounts[1], 5000, 5000);
        await CheckDepositEvent(oracleFeeWalletInst, accounts[2], 10000, 10000);
        await CheckDepositEvent(oracleFeeWalletInst, accounts[1], 7000, 12000);
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
            value: BigNumber(web3.toWei(2)).toNumber(),
        });
        await oracleFeeWalletInst.deposit({
            from: accounts[2],
            value: BigNumber(web3.toWei(3)).toNumber(),
        });

        await oracleFeeWalletInst.registerClientAddr(
            accounts[3],
            { from: accounts[0] },
        );
        await oracleFeeWalletInst.registerClientAddr(
            accounts[4],
            { from: accounts[0] },
        );

        const helperInfos = [{
            addr: accounts[3],
            accumulateValue: BigNumber(0),
        }, {
            addr: accounts[4],
            accumulateValue: BigNumber(0),
        }];

        const usedInfos = [{
            addr: accounts[1],
            accumulateValue: await oracleFeeWalletInst.getBalance.call(accounts[1]),
        }, {
            addr: accounts[2],
            accumulateValue: await oracleFeeWalletInst.getBalance.call(accounts[2]),
        }];

        // use account1 and update in account3
        let sentValue = BigNumber(web3.toWei(0.1));
        let afterInfoDict = UpdateUsedBalance(sentValue, usedInfos[0], helperInfos[0]);
        usedInfos[0] = afterInfoDict.usedInfo;
        helperInfos[0] = afterInfoDict.helperInfo;
        await CheckUpdateUsedBalanceEvent(
            oracleFeeWalletInst,
            sentValue,
            usedInfos[0],
            helperInfos[0],
        );

        // use account1 and update in account3
        sentValue = BigNumber(web3.toWei(0.2));
        afterInfoDict = UpdateUsedBalance(sentValue, usedInfos[0], helperInfos[0]);
        usedInfos[0] = afterInfoDict.usedInfo;
        helperInfos[0] = afterInfoDict.helperInfo;
        await CheckUpdateUsedBalanceEvent(
            oracleFeeWalletInst,
            sentValue,
            usedInfos[0],
            helperInfos[0],
        );

        // use account2 and update in account3
        sentValue = BigNumber(web3.toWei(0.3));
        afterInfoDict = UpdateUsedBalance(sentValue, usedInfos[1], helperInfos[0]);
        usedInfos[1] = afterInfoDict.usedInfo;
        helperInfos[0] = afterInfoDict.helperInfo;
        await CheckUpdateUsedBalanceEvent(
            oracleFeeWalletInst,
            sentValue,
            usedInfos[1],
            helperInfos[0],
        );

        // use account2 and update in account4
        sentValue = BigNumber(web3.toWei(0.4));
        afterInfoDict = UpdateUsedBalance(sentValue, usedInfos[1], helperInfos[1]);
        usedInfos[1] = afterInfoDict.usedInfo;
        helperInfos[1] = afterInfoDict.helperInfo;
        await CheckUpdateUsedBalanceEvent(
            oracleFeeWalletInst,
            sentValue,
            usedInfos[1],
            helperInfos[1],
        );

        TestUtils.AssertRevert(oracleFeeWalletInst.updateUsedBalance(
            accounts[8],
            web3.toWei(1000), {
                from: accounts[0],
            },
        ));

        const paybackInfos = [{
            addr: helperInfos[0].addr,
            accumulateValue: helperInfos[0].accumulateValue,
            balance: await web3.eth.getBalance(helperInfos[0].addr),
        }, {
            addr: helperInfos[1].addr,
            accumulateValue: helperInfos[1].accumulateValue,
            balance: await web3.eth.getBalance(helperInfos[1].addr),
        }];
        // Because payback is from lastest to oldest
        await CheckPaybackEvent(
            oracleFeeWalletInst,
            [paybackInfos[1], paybackInfos[0]],
            accounts[0],
        );

        const balanceInfos = [{
            balance: await web3.eth.getBalance(paybackInfos[0].addr),
        }, {
            balance: await web3.eth.getBalance(paybackInfos[1].addr),
        }];
        for (let i = 0; i < paybackInfos.length; i += 1) {
            assert.equal(
                balanceInfos[i].balance.toNumber(),
                paybackInfos[i].accumulateValue.plus(paybackInfos[i].balance).toNumber(),
                'balance should be the same',
            );
        }
    });

    it('Permission check test', async () => {
        const targetTestAddrs = [accounts[5], accounts[6]];
        await oracleFeeWalletInst.deposit({
            from: targetTestAddrs[0],
            value: BigNumber(web3.toWei(2)).toNumber(),
        });
        await oracleFeeWalletInst.deposit({
            from: targetTestAddrs[1],
            value: BigNumber(web3.toWei(2)).toNumber(),
        });

        TestUtils.AssertRevert(oracleFeeWalletInst.updateUsedBalance(
            targetTestAddrs[0],
            BigNumber(web3.toWei(0.1)).toNumber(),
            { from: targetTestAddrs[0] },
        ));

        await oracleFeeWalletInst.registerClientAddr(targetTestAddrs[0]);
        TestUtils.AssertPass(oracleFeeWalletInst.updateUsedBalance(
            targetTestAddrs[0],
            BigNumber(web3.toWei(0.1)).toNumber(),
            { from: targetTestAddrs[0] },
        ));
        await oracleFeeWalletInst.deregisterClientAddr(targetTestAddrs[0]);
        TestUtils.AssertRevert(oracleFeeWalletInst.updateUsedBalance(
            targetTestAddrs[0],
            BigNumber(web3.toWei(0.1)).toNumber(),
            { from: targetTestAddrs[0] },
        ));

        await oracleFeeWalletInst.registerClientAddr(targetTestAddrs[0]);
        TestUtils.AssertPass(oracleFeeWalletInst.updateUsedBalance(
            targetTestAddrs[0],
            BigNumber(web3.toWei(0.1)).toNumber(),
            { from: targetTestAddrs[0] },
        ));
        await oracleFeeWalletInst.registerClientAddr(targetTestAddrs[1]);
        TestUtils.AssertPass(oracleFeeWalletInst.updateUsedBalance(
            targetTestAddrs[1],
            BigNumber(web3.toWei(0.1)).toNumber(),
            { from: targetTestAddrs[1] },
        ));
        await oracleFeeWalletInst.deregisterClientAddr(targetTestAddrs[0]);
        TestUtils.AssertRevert(oracleFeeWalletInst.updateUsedBalance(
            targetTestAddrs[0],
            BigNumber(web3.toWei(0.1)).toNumber(),
            { from: targetTestAddrs[0] },
        ));
        await oracleFeeWalletInst.deregisterClientAddr(targetTestAddrs[1]);
        TestUtils.AssertRevert(oracleFeeWalletInst.updateUsedBalance(
            targetTestAddrs[1],
            BigNumber(web3.toWei(0.1)).toNumber(),
            { from: targetTestAddrs[1] },
        ));
        await oracleFeeWalletInst.registerClientAddr(targetTestAddrs[1]);
        TestUtils.AssertPass(oracleFeeWalletInst.updateUsedBalance(
            targetTestAddrs[1],
            BigNumber(web3.toWei(0.1)).toNumber(),
            { from: targetTestAddrs[1] },
        ));
    });
});
