/* global artifacts */

const OracleRegister = artifacts.require('./OracleRegister');
const OracleStorage = artifacts.require('./OracleStorage');
const TestStorage = artifacts.require('./TestStorage');
const OracleCore = artifacts.require('./OracleCore');
const TestOracleExample = artifacts.require('./TestOracleExample');

module.exports = (deployer, network, accounts) => {
    let oracleStorageInst = null;
    let oracleCoreInst = null;
    let oracleRegisterInst = null;
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
            return deployer.deploy(
                OracleRegister,
                accounts[0],
                oracleStorageInst.address,
            );
        })
        .then((inst) => {
            oracleRegisterInst = inst;
            console.log(`OracleRegsiter address: ${inst.address}`);
            return deployer.deploy(
                OracleCore,
                accounts[0],
                oracleRegisterInst.address,
            );
        })
        .then((inst) => {
            console.log(`OracleCore address: ${inst.address}`);
            oracleCoreInst = inst;
            return deployer.deploy(
                TestOracleExample,
                accounts[0],
                oracleRegisterInst.address,
                TestStorage.address,
            );
        })
        .then((inst) => {
            console.log(`TestOracleExample address: ${inst.address}`);
            return oracleStorageInst.setOracleRegisterAddr(
                oracleRegisterInst.address,
                { from: accounts[0] },
            );
        })
        .then(() => {
            return oracleRegisterInst.registAddress(
                'OracleCore',
                oracleCoreInst.address,
                { from: accounts[0] },
            );
        })
        .then(() => {
            return oracleRegisterInst.registAddress(
                'OracleStorage',
                oracleStorageInst.address,
                { from: accounts[0] },
            );
        })
        .then(() => {
            console.log('Finish deploy');
        });
};
