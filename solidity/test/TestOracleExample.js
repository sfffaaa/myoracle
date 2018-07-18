/* eslint no-underscore-dangle: ["error", { "allow": ["__querySentNode", "__callback"] }] */
/* global artifacts, contract, it, assert, web3 */

const TestUtils = require('./TestUtils.js');

const OracleCore = artifacts.require('OracleCore');
const TestOracleExample = artifacts.require('TestOracleExample');

contract('TestOracleExample', (accounts) => {
    const FAKE_REQUEST = "Whatever doesn't kill you";
    const FAKE_RESPONSE = 'simply makes you stranger';

    it('trigger test', async () => {
        const oracleCoreInst = await OracleCore.deployed();
        const testOracleExampleInst = await TestOracleExample.deployed();

        await testOracleExampleInst.trigger(
            {
                value: TestUtils.ALLOW_PAYMENT_VALUE,
                from: accounts[0],
            },
        );
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


        TestUtils.AssertPass(testOracleExampleInst.trigger(
            {
                value: TestUtils.ALLOW_PAYMENT_VALUE,
                from: accounts[0],
            },
        ));
        TestUtils.AssertRevert(testOracleExampleInst.trigger(
            {
                value: TestUtils.ALLOW_PAYMENT_VALUE,
                from: accounts[1],
            },
        ));

        TestUtils.AssertPass(testOracleExampleInst.getLastestQueryId({ from: accounts[0] }));
        TestUtils.AssertRevert(testOracleExampleInst.getLastestQueryId({ from: accounts[1] }));

        TestUtils.AssertPass(testOracleExampleInst.__querySentNode(
            FAKE_REQUEST,
            {
                value: TestUtils.ALLOW_PAYMENT_VALUE,
                from: accounts[0],
            },
        ));
        TestUtils.AssertRevert(testOracleExampleInst.__querySentNode(
            FAKE_REQUEST,
            {
                value: TestUtils.ALLOW_PAYMENT_VALUE,
                from: accounts[1],
            },
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
    it('oracleCoreInst permission test', async () => {
        const oracleCoreInst = await OracleCore.deployed();
        const testOracleExampleInst = await TestOracleExample.deployed();

        await testOracleExampleInst.trigger(
            {
                value: TestUtils.ALLOW_PAYMENT_VALUE,
                from: accounts[0],
            },
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
});
