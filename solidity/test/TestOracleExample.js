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
    const oracleOwner = accounts[1];
    const testOwner = accounts[2];
    const otherUser = accounts[3];

    before(async () => {
        oracleCoreInst = await OracleCore.deployed();
        testOracleExampleInst = await TestOracleExample.deployed();
    });

    it('wallet check', async () => {
        TestUtils.AssertPass(testOracleExampleInst.deposit({
            value: 20000,
            from: testOwner,
        }));
        await testOracleExampleInst.trigger({ from: testOwner });
        await testOracleExampleInst.trigger({ from: testOwner });
        TestUtils.AssertRevert(testOracleExampleInst.trigger({ from: testOwner }));
    });

    it('trigger test', async () => {
        TestUtils.AssertPass(testOracleExampleInst.deposit({
            value: 10000,
            from: testOwner,
        }));
        await testOracleExampleInst.trigger({ from: testOwner });
        let oracleData = {};
        const toOracleNodeEvent = oracleCoreInst.ToOracleNode({}, { fromBlock: 0, toBlock: 'latest' });
        const oracleLogs = await TestUtils.WaitContractEventGet(toOracleNodeEvent);
        oracleData = oracleLogs[oracleLogs.length - 1].args;
        assert.equal(oracleData.request,
            'json(https://api.kraken.com/0/public/Ticker?pair=ETHUSD)["result"]["XETHZUSD"]["c"][0]',
            'Request should be the same');

        const queryId = await testOracleExampleInst.getLastestQueryId({ from: testOwner });
        assert.equal(oracleData.queryId, queryId, 'QueryId should be the same');
    });

    it('permission check', async () => {
        TestUtils.AssertPass(testOracleExampleInst.deposit({
            value: 20000,
            from: testOwner,
        }));
        await testOracleExampleInst.trigger({ from: testOwner });
        TestUtils.AssertRevert(testOracleExampleInst.trigger({ from: otherUser }));

        await testOracleExampleInst.getLastestQueryId({ from: testOwner });
        TestUtils.AssertRevert(testOracleExampleInst.getLastestQueryId({ from: otherUser }));

        await testOracleExampleInst.__querySentNode(
            0,
            FAKE_REQUEST,
            { from: testOwner },
        );
        TestUtils.AssertRevert(testOracleExampleInst.__querySentNode(
            0,
            FAKE_REQUEST,
            { from: otherUser },
        ));

        const fakeQueryId = web3.sha3(FAKE_RESPONSE);
        await testOracleExampleInst.__callback(
            fakeQueryId,
            FAKE_REQUEST,
            fakeQueryId,
            { from: testOwner },
        );

        TestUtils.AssertRevert(testOracleExampleInst.__callback(
            fakeQueryId,
            FAKE_REQUEST,
            fakeQueryId,
            { from: otherUser },
        ));
    });
    it('oracleCoreInst permission test', async () => {
        TestUtils.AssertPass(testOracleExampleInst.deposit({
            value: 20000,
            from: testOwner,
        }));
        await testOracleExampleInst.trigger({ from: testOwner });
        const queryId = await testOracleExampleInst.getLastestQueryId({ from: testOwner });

        await oracleCoreInst.resultSentBack(
            queryId,
            FAKE_RESPONSE,
            web3.sha3(FAKE_RESPONSE),
            { from: oracleOwner },
        );
        TestUtils.AssertRevert(oracleCoreInst.resultSentBack(
            queryId,
            FAKE_RESPONSE,
            web3.sha3(FAKE_RESPONSE),
            { from: otherUser },
        ));
    });

    it('test oracle example payment test', async () => {
        await testOracleExampleInst.deposit({
            value: 10000,
            from: testOwner,
        });
        await testOracleExampleInst.trigger({ from: testOwner });
        TestUtils.AssertRevert(testOracleExampleInst.trigger({ from: testOwner }));
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
