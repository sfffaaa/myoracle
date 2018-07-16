/* global artifacts */

const OracleStorage = artifacts.require('./OracleStorage');
const TestStorage = artifacts.require('./TestStorage');
const OracleCore = artifacts.require('./OracleCore');
const TestOracleExample = artifacts.require('./TestOracleExample');

module.exports = (deployer, network, accounts) => {
    let oracleStorageInst = null;
    let oracleCoreInst = null;
    deployer.deploy(TestStorage).then((inst) => {
        console.log(`TestStorage address: ${inst.address}`);
        return deployer.deploy(
            OracleStorage,
            accounts[0],
        );
    })
        .then((inst) => {
            console.log(`OracleStorage address: ${inst.address}`);
            oracleStorageInst = inst;
            return deployer.deploy(OracleCore, accounts[0], inst.address);
        })
        .then((inst) => {
            console.log(`OracleCore address: ${inst.address}`);
            oracleCoreInst = inst;
            return deployer.deploy(
                TestOracleExample,
                accounts[0],
                OracleStorage.address,
                TestStorage.address,
            );
        })
        .then((inst) => {
            console.log(`TestOracleExample address: ${inst.address}`);
            return oracleStorageInst.setOracleCoreAddr(
                oracleCoreInst.address,
                { from: accounts[0] },
            );
        })
        .then(() => {
            return oracleCoreInst.setOracleCoreAddr(
                { from: accounts[0] },
            );
        });
};
