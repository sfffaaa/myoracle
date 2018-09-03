/* eslint no-underscore-dangle: ["error", { "allow": ["__querySentNode", "__callback"] }] */
/* global artifacts, contract, it, assert, web3, before */

const TestUtils = require('./TestUtils.js');

const OracleCore = artifacts.require('OracleCore');
const TestOracleExample = artifacts.require('TestOracleExample');

contract('TestOracleExample', (accounts) => {
    const FAKE_REQUEST = "Whatever doesn't kill you";
    const FAKE_RESPONSE = 'simply makes you stranger';
    let oracleCoreInst = null;
    let testOracleExampleInst = null;

    before(async () => {
        oracleCoreInst = await OracleCore.deployed();
        testOracleExampleInst = await TestOracleExample.deployed();
    });

    it('wallet check', async () => {
        TestUtils.AssertPass(testOracleExampleInst.deposit({
            value: 20000,
        }));
        TestUtils.AssertPass(testOracleExampleInst.trigger(
            {
                value: TestUtils.ALLOW_PAYMENT_VALUE,
                from: accounts[0],
            },
        ));
        TestUtils.AssertPass(testOracleExampleInst.trigger(
            {
                value: TestUtils.ALLOW_PAYMENT_VALUE,
                from: accounts[0],
            },
        ));
        TestUtils.AssertRevert(testOracleExampleInst.trigger(
            {
                value: TestUtils.ALLOW_PAYMENT_VALUE,
                from: accounts[0],
            },
        ));
    });

    it('trigger test', async () => {
        TestUtils.AssertPass(testOracleExampleInst.deposit({
            value: 10000,
        }));
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
        TestUtils.AssertPass(testOracleExampleInst.deposit({
            value: 20000,
        }));
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
            0,
            FAKE_REQUEST,
            {
                value: TestUtils.ALLOW_PAYMENT_VALUE,
                from: accounts[0],
            },
        ));
        TestUtils.AssertRevert(testOracleExampleInst.__querySentNode(
            0,
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
        TestUtils.AssertPass(testOracleExampleInst.deposit({
            value: 20000,
        }));
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

    it('test oracle example payment test', async () => {
        TestUtils.AssertPass(testOracleExampleInst.deposit({
            value: 10000,
        }));
        TestUtils.AssertPass(testOracleExampleInst.trigger(
            {
                value: TestUtils.ALLOW_PAYMENT_VALUE,
                from: accounts[0],
            },
        ));
        TestUtils.AssertRevert(testOracleExampleInst.trigger(
            {
                value: 1000000,
                from: accounts[0],
            },
        ));
        TestUtils.AssertRevert(testOracleExampleInst.trigger(
            {
                value: 1,
                from: accounts[0],
            },
        ));
    });

    it('convert check', async () => {
        const result = [
            ['123', true, 123],
            ['123.123', true, 123],
            ['a123', false, 0],
            ['aas', false, 0],
            ['123a', false, 0],
        ];
        const reqs = [];
        for (let i = 0; i < result.length; i += 1) {
            reqs.push(testOracleExampleInst.convertResponseToPrice.call(result[i][0]));
        }
        const resps = await Promise.all(reqs);
        for (let i = 0; i < result.length; i += 1) {
            assert.equal(resps[i][0], result[i][1], 'convert success');
            assert.equal(resps[i][1], result[i][2], 'price checking');
        }
    });
});
