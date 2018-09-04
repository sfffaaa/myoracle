/* global artifacts, contract, it, web3, assert, before */

const OracleCore = artifacts.require('OracleCore');
const TestOracleExample = artifacts.require('TestOracleExample');
const truffleAssert = require('truffle-assertions');
const TestUtils = require('./TestUtils.js');


contract('OracleCoreBasic', (accounts) => {
    const FAKE_REQUEST = "Whatever doesn't kill you";
    const FAKE_RESPONSE = 'simply makes you stranger';
    let oracleCoreInst = null;
    let testOracleExampleInst = null;

    before(async () => {
        oracleCoreInst = await OracleCore.deployed();
        testOracleExampleInst = await TestOracleExample.deployed();
    });

    it('Basic test', async () => {
        console.log(`OracleCore: ${OracleCore.address}`);
        console.log(`TestOracleExample: ${TestOracleExample.address}`);

        TestUtils.AssertPass(testOracleExampleInst.deposit({
            value: 20000,
        }));

        let queryId = 0;
        let tx = await oracleCoreInst.querySentNode(
            0,
            testOracleExampleInst.address,
            FAKE_REQUEST,
            { from: accounts[0] },
        );
        truffleAssert.eventEmitted(tx, 'ToOracleNode', (ev) => {
            const { queryId: queryIdTmp } = ev;
            queryId = queryIdTmp;
            return true;
        });

        tx = await oracleCoreInst.resultSentBack(
            queryId,
            FAKE_RESPONSE,
            web3.sha3(FAKE_RESPONSE),
        );
        truffleAssert.eventEmitted(tx, 'ToOracleCallee', (ev) => {
            return ev.queryId === queryId && ev.callee === TestOracleExample.address;
        });

        let oracleData = {};
        const toOracleCalleeEvent = oracleCoreInst.ToOracleCallee({}, { fromBlock: 0, toBlock: 'latest' });
        const oracleLogs = await TestUtils.WaitContractEventGet(toOracleCalleeEvent);
        oracleData = oracleLogs[oracleLogs.length - 1].args;

        let calleeData = {};
        const showCallbackEvent = testOracleExampleInst.ShowCallback({}, { fromBlock: 0, toBlock: 'latest' });
        const calleeLogs = await TestUtils.WaitContractEventGet(showCallbackEvent);
        calleeData = calleeLogs[calleeLogs.length - 1].args;
        calleeData.callee = testOracleExampleInst.address;
        if (TestUtils.CheckObjectEqual(oracleData, calleeData) === false) {
            assert.equal(oracleData, calleeData, 'Two object should be the same');
        }
    });

    it('oracleCoreInst permission test', async () => {
        TestUtils.AssertPass(testOracleExampleInst.deposit({
            value: 30000,
        }));
        await testOracleExampleInst.trigger(
            { from: accounts[0] },
        );
        const queryId = await testOracleExampleInst.getLastestQueryId({ from: accounts[0] });

        TestUtils.AssertPass(oracleCoreInst.resultSentBack(
            queryId,
            FAKE_RESPONSE,
            web3.sha3(FAKE_RESPONSE),
        ));
        TestUtils.AssertRevert(oracleCoreInst.resultSentBack(
            queryId,
            FAKE_RESPONSE,
            web3.sha3(FAKE_RESPONSE),
            { from: accounts[1] },
        ));
    });

    it('oracleCoreInst payment test', async () => {
        TestUtils.AssertPass(testOracleExampleInst.deposit({
            value: 30000,
        }));
        await testOracleExampleInst.trigger(
            { from: accounts[0] },
        );
        const queryId = await testOracleExampleInst.getLastestQueryId({ from: accounts[0] });

        TestUtils.AssertPass(oracleCoreInst.resultSentBack(
            queryId,
            FAKE_RESPONSE,
            web3.sha3(FAKE_RESPONSE),
        ));
        TestUtils.AssertRevert(oracleCoreInst.resultSentBack(
            queryId,
            FAKE_RESPONSE,
            web3.sha3(FAKE_RESPONSE),
            { from: accounts[1] },
        ));
    });

    it('Payment test', async () => {
        TestUtils.AssertPass(testOracleExampleInst.deposit({
            value: 10000,
        }));

        TestUtils.AssertPass(oracleCoreInst.querySentNode(
            0,
            testOracleExampleInst.address,
            'Why you are so serious???',
            { from: accounts[0] },
        ));
        TestUtils.AssertRevert(oracleCoreInst.querySentNode(
            0,
            testOracleExampleInst.address,
            FAKE_REQUEST,
            { from: accounts[0] },
        ));
    });
});
