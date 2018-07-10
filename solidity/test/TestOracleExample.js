/* global artifacts, contract, it, assert */
const TestUtils = require('./TestUtils.js');

const OracleCore = artifacts.require('OracleCore');
const TestOracleExample = artifacts.require('TestOracleExample');

contract('TestOracleExample', () => {
    it('querySentNode test', async () => {
        const oracleCoreInst = await OracleCore.deployed();
        const testOracleExampleInst = await TestOracleExample.deployed();

        await testOracleExampleInst.querySentNode('fake request');
        let oracleData = {};
        const toOracleNodeEvent = oracleCoreInst.ToOracleNode({}, { fromBlock: 0, toBlock: 'latest' });
        const oracleLogs = await TestUtils.WaitContractEventGet(toOracleNodeEvent);
        oracleData = oracleLogs[oracleLogs.length - 1].args;
        assert.equal(oracleData.requests, 'fake request', 'Request should be the same');

        const queryId = await testOracleExampleInst.getLastestQueryId();
        assert.equal(oracleData.queryId, queryId, 'QueryId should be the same');
    });
});
