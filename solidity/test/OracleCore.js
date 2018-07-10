/* global artifacts, contract, it, web3, assert */

const OracleCore = artifacts.require('OracleCore');
const TestOracleExample = artifacts.require('TestOracleExample');
const truffleAssert = require('truffle-assertions');
const TestUtils = require('./TestUtils.js');


contract('OracleCoreBasic', () => {
    it('Basic test', async () => {
        console.log(`OracleCore: ${OracleCore.address}`);
        console.log(`TestOracleExample: ${TestOracleExample.address}`);

        const oracleCoreInst = await OracleCore.deployed();
        const testOracleExampleInst = await TestOracleExample.deployed();

        let queryId = 0;
        let tx = await oracleCoreInst.querySentNode(testOracleExampleInst.address, 'fake request');
        truffleAssert.eventEmitted(tx, 'ToOracleNode', (ev) => {
            const { queryId: queryIdTmp } = ev;
            queryId = queryIdTmp;
            return true;
        });

        tx = await oracleCoreInst.resultSentBack(queryId, 'fake response', web3.sha3('fake response'));
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
});
