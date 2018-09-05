/* global artifacts, contract, it, web3, assert, before */

const OracleCore = artifacts.require('OracleCore');
const HodlOracle = artifacts.require('HodlOracle');
const truffleAssert = require('truffle-assertions');
const TestUtils = require('./TestUtils.js');


contract('OracleCoreBasic', (accounts) => {
    const FAKE_REQUEST = "Whatever doesn't kill you";
    const FAKE_RESPONSE = 'simply makes you stranger';
    let oracleCoreInst = null;
    let hodlOracleInst = null;
    const oracleOwner = accounts[1];
    const hodlOwner = accounts[2];
    const otherUser = accounts[3];

    before(async () => {
        oracleCoreInst = await OracleCore.deployed();
        hodlOracleInst = await HodlOracle.deployed();
    });

    it('Basic test', async () => {
        console.log(`OracleCore: ${OracleCore.address}`);
        console.log(`HodlOracle: ${HodlOracle.address}`);

        TestUtils.AssertPass(hodlOracleInst.deposit({
            value: 20000,
            from: hodlOwner,
        }));

        let queryId = 0;
        let tx = await oracleCoreInst.querySentNode(
            0,
            hodlOracleInst.address,
            FAKE_REQUEST,
            { from: oracleOwner },
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
            { from: oracleOwner },
        );
        truffleAssert.eventEmitted(tx, 'ToOracleCallee', (ev) => {
            return ev.queryId === queryId && ev.callee === HodlOracle.address;
        });

        let oracleData = {};
        const toOracleCalleeEvent = oracleCoreInst.ToOracleCallee({}, { fromBlock: 0, toBlock: 'latest' });
        const oracleLogs = await TestUtils.WaitContractEventGet(toOracleCalleeEvent);
        oracleData = oracleLogs[oracleLogs.length - 1].args;

        let calleeData = {};
        const showCallbackEvent = hodlOracleInst.ShowCallback({}, { fromBlock: 0, toBlock: 'latest' });
        const calleeLogs = await TestUtils.WaitContractEventGet(showCallbackEvent);
        calleeData = calleeLogs[calleeLogs.length - 1].args;
        calleeData.callee = hodlOracleInst.address;
        if (TestUtils.CheckObjectEqual(oracleData, calleeData) === false) {
            assert.equal(oracleData, calleeData, 'Two object should be the same');
        }
    });

    it('oracleCoreInst permission test', async () => {
        TestUtils.AssertPass(hodlOracleInst.deposit({
            value: 30000,
            from: hodlOwner,
        }));
        await hodlOracleInst.trigger(
            { from: hodlOwner },
        );
        const queryId = await hodlOracleInst.getLastestQueryId({ from: hodlOwner });

        TestUtils.AssertPass(oracleCoreInst.resultSentBack(
            queryId,
            FAKE_RESPONSE,
            web3.sha3(FAKE_RESPONSE),
            { from: oracleOwner },
        ));
        TestUtils.AssertRevert(oracleCoreInst.resultSentBack(
            queryId,
            FAKE_RESPONSE,
            web3.sha3(FAKE_RESPONSE),
            { from: otherUser },
        ));
    });

    it('oracleCoreInst payment test', async () => {
        TestUtils.AssertPass(hodlOracleInst.deposit({
            value: 30000,
            from: hodlOwner,
        }));
        await hodlOracleInst.trigger(
            { from: hodlOwner },
        );
        const queryId = await hodlOracleInst.getLastestQueryId({ from: hodlOwner });

        TestUtils.AssertPass(oracleCoreInst.resultSentBack(
            queryId,
            FAKE_RESPONSE,
            web3.sha3(FAKE_RESPONSE),
            { from: oracleOwner },
        ));
        TestUtils.AssertRevert(oracleCoreInst.resultSentBack(
            queryId,
            FAKE_RESPONSE,
            web3.sha3(FAKE_RESPONSE),
            { from: otherUser },
        ));
    });

    it('Payment test', async () => {
        TestUtils.AssertPass(hodlOracleInst.deposit({
            value: 10000,
            from: hodlOwner,
        }));

        TestUtils.AssertPass(oracleCoreInst.querySentNode(
            0,
            hodlOracleInst.address,
            'Why you are so serious???',
            { from: oracleOwner },
        ));
        TestUtils.AssertRevert(oracleCoreInst.querySentNode(
            0,
            hodlOracleInst.address,
            FAKE_REQUEST,
            { from: oracleOwner },
        ));
    });
});
