/* eslint no-underscore-dangle: ["error", { "allow": ["__querySentNode", "__callback"] }] */
/* global artifacts, contract, it, assert, web3 */

const truffleAssert = require('truffle-assertions');
const TestUtils = require('./TestUtils.js');

const OracleCore = artifacts.require('OracleCore');
const TestOracleExample = artifacts.require('TestOracleExample');

contract('TestOracleExample', (accounts) => {
    const FAKE_REQUEST = "Whatever doesn't kill you";
    const FAKE_RESPONSE = 'simply makes you stranger';

    it('querySentNode test', async () => {
        const oracleCoreInst = await OracleCore.deployed();
        const testOracleExampleInst = await TestOracleExample.deployed();

        await testOracleExampleInst.querySentNode(FAKE_REQUEST, { from: accounts[0] });
        let oracleData = {};
        const toOracleNodeEvent = oracleCoreInst.ToOracleNode({}, { fromBlock: 0, toBlock: 'latest' });
        let oracleLogs = await TestUtils.WaitContractEventGet(toOracleNodeEvent);
        oracleData = oracleLogs[oracleLogs.length - 1].args;
        assert.equal(oracleData.request, FAKE_REQUEST, 'Request should be the same');

        const queryId = await testOracleExampleInst.getLastestQueryId({ from: accounts[0] });
        assert.equal(oracleData.queryId, queryId, 'QueryId should be the same');

        // Simulate respone without running node
        const tx = await oracleCoreInst.resultSentBack(
            queryId,
            FAKE_RESPONSE,
            web3.sha3(FAKE_RESPONSE),
        );
        truffleAssert.eventEmitted(tx, 'ToOracleCallee', (ev) => {
            return ev.queryId === queryId && ev.callee === TestOracleExample.address;
        });

        const toOracleCalleeEvent = oracleCoreInst.ToOracleCallee({}, { fromBlock: 0, toBlock: 'latest' });
        oracleLogs = await TestUtils.WaitContractEventGet(toOracleCalleeEvent);
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

    it('trigger test', async () => {
        const oracleCoreInst = await OracleCore.deployed();
        const testOracleExampleInst = await TestOracleExample.deployed();

        await testOracleExampleInst.trigger({ from: accounts[0] });
        let oracleData = {};
        const toOracleNodeEvent = oracleCoreInst.ToOracleNode({}, { fromBlock: 0, toBlock: 'latest' });
        const oracleLogs = await TestUtils.WaitContractEventGet(toOracleNodeEvent);
        oracleData = oracleLogs[oracleLogs.length - 1].args;
        assert.equal(oracleData.request,
            'json(https://api.kraken.com/0/public/Ticker?pair=ETHUSD)["result"]["XETHZUSD"]["c"][0]',
            'Request should be the same');

        const queryId = await testOracleExampleInst.getLastestQueryId({ from: accounts[0] });
        assert.equal(oracleData.queryId, queryId, 'QueryId should be the same');
    });

    it('permission check', async () => {
        const testOracleExampleInst = await TestOracleExample.deployed();

        TestUtils.AssertPass(testOracleExampleInst.querySentNode(
            FAKE_REQUEST,
            { from: accounts[0] },
        ));
        TestUtils.AssertRevert(testOracleExampleInst.querySentNode(
            FAKE_REQUEST,
            { from: accounts[1] },
        ));
        TestUtils.AssertPass(testOracleExampleInst.getLastestQueryId({ from: accounts[0] }));
        TestUtils.AssertPass(testOracleExampleInst.getLastestQueryId({ from: accounts[1] }));

        TestUtils.AssertPass(testOracleExampleInst.trigger({ from: accounts[0] }));
        TestUtils.AssertPass(testOracleExampleInst.trigger({ from: accounts[1] }));
        TestUtils.AssertPass(testOracleExampleInst.__querySentNode(
            FAKE_REQUEST,
            { from: accounts[0] },
        ));
        TestUtils.AssertRevert(testOracleExampleInst.__querySentNode(
            FAKE_REQUEST,
            { from: accounts[1] },
        ));

        const fakeQueryId = web3.sha3(FAKE_RESPONSE);
        TestUtils.AssertPass(testOracleExampleInst.__callback(
            fakeQueryId,
            FAKE_REQUEST,
            fakeQueryId,
            { from: accounts[0] },
        ));

        TestUtils.AssertRevert(testOracleExampleInst.__callback(
            fakeQueryId,
            FAKE_REQUEST,
            fakeQueryId,
            { from: accounts[1] },
        ));
    });
});
