/* global artifacts */

const OracleStorage = artifacts.require('./OracleStorage');
const OracleCore = artifacts.require('./OracleCore');
const TestOracleExample = artifacts.require('./TestOracleExample');

module.exports = (deployer, network, accounts) => {
    deployer.deploy(OracleStorage).then((inst) => {
        console.log(`OracleStorage address: ${inst.address}`);
        return deployer.deploy(OracleCore, inst.address);
    }).then((inst) => {
        console.log(`OracleCore address: ${inst.address}`);
        return deployer.deploy(TestOracleExample, accounts[0], OracleStorage.address);
    }).then((inst) => {
        console.log(`TestOracleExample address: ${inst.address}`);
        // do nothing right now
    });
};
