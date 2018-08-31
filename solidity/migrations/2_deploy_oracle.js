/* global artifacts */

const OracleRegister = artifacts.require('./OracleRegister');
const OracleStorage = artifacts.require('./OracleStorage');
const OracleCore = artifacts.require('./OracleCore');
const OracleWallet = artifacts.require('./OracleWallet');

const TestStorage = artifacts.require('./TestStorage');
const TestWalletDistributor = artifacts.require('./TestWalletDistributor');
const TestRegister = artifacts.require('./TestRegister');
const TestOracleExample = artifacts.require('./TestOracleExample');


module.exports = (deployer, network, accounts) => {
    let oracleStorageInst = null;
    let oracleCoreInst = null;
    let oracleRegisterInst = null;
    let oracleWalletInst = null;
    let testStorageInst = null;
    let testWalletDistributorInst = null;
    let testOracleExampleInst = null;
    let testRegisterInst = null;

    deployer.deploy(TestStorage, accounts[0]).then((inst) => {
        console.log(`TestStorage address: ${inst.address}`);
        testStorageInst = inst;
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
                OracleWallet,
                accounts[0],
            );
        })
        .then((inst) => {
            console.log(`OracleWallet address: ${inst.address}`);
            oracleWalletInst = inst;
            return deployer.deploy(
                TestRegister,
                accounts[0],
            );
        })
        .then((inst) => {
            console.log(`TestRegister address: ${inst.address}`);
            testRegisterInst = inst;
            return deployer.deploy(
                TestWalletDistributor,
                accounts[0],
                testRegisterInst.address,
            );
        })
        .then((inst) => {
            console.log(`TestWalletDistributor address: ${inst.address}`);
            testWalletDistributorInst = inst;
            return deployer.deploy(
                TestOracleExample,
                accounts[0],
                oracleRegisterInst.address,
                testRegisterInst.address,
            );
        })
        .then((inst) => {
            console.log(`TestOracleExample address: ${inst.address}`);
            testOracleExampleInst = inst;
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
            return oracleRegisterInst.registAddress(
                'OracleWallet',
                oracleWalletInst.address,
                { from: accounts[0] },
            );
        })
        .then(() => {
            return testRegisterInst.registAddress(
                'TestWalletDistributor',
                testWalletDistributorInst.address,
                { from: accounts[0] },
            );
        })
        .then(() => {
            return testRegisterInst.registAddress(
                'TestOracleExample',
                testOracleExampleInst.address,
                { from: accounts[0] },
            );
        })
        .then(() => {
            return testRegisterInst.registAddress(
                'TestStorage',
                testStorageInst.address,
                { from: accounts[0] },
            );
        })
        .then(() => {
            return testStorageInst.setAllower(
                testWalletDistributorInst.address,
                { from: accounts[0] },
            );
        })
        .then(() => {
            return testStorageInst.setAllower(
                testOracleExampleInst.address,
                { from: accounts[0] },
            );
        })
        .then(() => {
            console.log('Finish deploy');
        });
};
