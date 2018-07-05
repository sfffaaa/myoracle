/* global artifacts, contract, it, web3, assert */

const OracleCore = artifacts.require('OracleCore');
const TestOracleExample = artifacts.require('TestOracleExample');
const truffleAssert = require('truffle-assertions');

const WaitContractEventGet = (myevent) => {
    return new Promise((resolve, reject) => {
        myevent.get((error, resp) => {
            if (error !== null) {
                reject(error);
            }
            resolve(resp);
        });
    });
};

const CheckObjectEqual = (ol, or) => {
    const olKeys = Object.keys(ol).sort();
    const orKeys = Object.keys(or).sort();

    if (olKeys.length !== orKeys.length) {
        console.log(`show me compare result: ${olKeys} v.s. ${orKeys}`);
        return false;
    }

    for (let i = 0; i < olKeys.length; i += 1) {
        const olKey = olKeys[i];
        const orKey = orKeys[i];
        if (olKey !== orKey || ol[olKey] !== or[orKey]) {
            console.log(`show me compare result ${olKey}: ${ol[olKey]} v.s. ${orKey}: ${or[orKey]}`);
            return false;
        }
    }
    return true;
};

contract('OracleCoreBasic', () => {
    it('Basic test', async () => {
        console.log(`OracleCore: ${OracleCore.address}`);
        console.log(`TestOracleExample: ${TestOracleExample.address}`);

        const oracleCoreInst = await OracleCore.deployed();
        const testOracleExampleInst = await TestOracleExample.deployed();

        let queryId = 0;
        let tx = await oracleCoreInst.QuerySentNode(testOracleExampleInst.address, 'fake request');
        truffleAssert.eventEmitted(tx, 'ToOracleNode', (ev) => {
            const { queryId: queryIdTmp } = ev;
            queryId = queryIdTmp;
            return true;
        });

        tx = await oracleCoreInst.ResultSentBack(queryId, 'fake response', web3.sha3('fake response'));
        truffleAssert.eventEmitted(tx, 'ToOracleCallee', (ev) => {
            return ev.queryId === queryId && ev.callee === TestOracleExample.address;
        });

        let oracleData = {};
        const toOracleCalleeEvent = oracleCoreInst.ToOracleCallee({}, { fromBlock: 0, toBlock: 'latest' });
        const oracleLogs = await WaitContractEventGet(toOracleCalleeEvent);
        oracleData = oracleLogs[oracleLogs.length - 1].args;

        let calleeData = {};
        const showCallbackEvent = testOracleExampleInst.ShowCallback({}, { fromBlock: 0, toBlock: 'latest' });
        const calleeLogs = await WaitContractEventGet(showCallbackEvent);
        calleeData = calleeLogs[calleeLogs.length - 1].args;
        calleeData.callee = testOracleExampleInst.address;
        if (CheckObjectEqual(oracleData, calleeData) === false) {
            assert.equal(oracleData, calleeData, 'Two object should be the same');
        }
    });
});
