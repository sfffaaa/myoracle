/* global artifacts */

const OracleRegister = artifacts.require('./OracleRegister');
const OracleStorage = artifacts.require('./OracleStorage');
const OracleCore = artifacts.require('./OracleCore');
const OracleWallet = artifacts.require('./OracleWallet');
const OracleFeeWallet = artifacts.require('./OracleFeeWallet');

const TestStorage = artifacts.require('./TestStorage');
const TestWalletDistributor = artifacts.require('./TestWalletDistributor');
const TestRegister = artifacts.require('./TestRegister');
const TestOracleExample = artifacts.require('./TestOracleExample');


module.exports = (deployer, network, accounts) => {
    let oracleStorageInst = null;
    let oracleCoreInst = null;
    let oracleRegisterInst = null;
    let oracleWalletInst = null;
    let oracleFeeWalletInst = null;

    let testStorageInst = null;
    let testWalletDistributorInst = null;
    let testOracleExampleInst = null;
    let testRegisterInst = null;

    const oracleOwner = accounts[1];
    const testOwner = accounts[2];

    deployer.deploy(TestStorage, testOwner).then((inst) => {
        console.log(`TestStorage address: ${inst.address}`);
        testStorageInst = inst;
        return deployer.deploy(
            OracleStorage,
            oracleOwner,
        );
    })
        .then((inst) => {
            console.log(`OracleStorage address: ${inst.address}`);
            oracleStorageInst = inst;
            return deployer.deploy(
                OracleRegister,
                oracleOwner,
            );
        })
        .then((inst) => {
            oracleRegisterInst = inst;
            console.log(`OracleRegsiter address: ${inst.address}`);
            return deployer.deploy(
                OracleCore,
                oracleOwner,
                oracleRegisterInst.address,
            );
        })
        .then((inst) => {
            console.log(`OracleCore address: ${inst.address}`);
            oracleCoreInst = inst;
            return deployer.deploy(
                OracleWallet,
                oracleOwner,
                oracleRegisterInst.address,
            );
        })
        .then((inst) => {
            console.log(`OracleWallet address: ${inst.address}`);
            oracleWalletInst = inst;
            return deployer.deploy(
                OracleFeeWallet,
                oracleOwner,
            );
        })
        .then((inst) => {
            console.log(`OracleFeeWallet address: ${inst.address}`);
            oracleFeeWalletInst = inst;
            return deployer.deploy(
                TestRegister,
                testOwner,
            );
        })
        .then((inst) => {
            console.log(`TestRegister address: ${inst.address}`);
            testRegisterInst = inst;
            return deployer.deploy(
                TestWalletDistributor,
                testOwner,
                testRegisterInst.address,
            );
        })
        .then((inst) => {
            console.log(`TestWalletDistributor address: ${inst.address}`);
            testWalletDistributorInst = inst;
            return deployer.deploy(
                TestOracleExample,
                testOwner,
                oracleRegisterInst.address,
                testRegisterInst.address,
            );
        })
        .then((inst) => {
            console.log(`TestOracleExample address: ${inst.address}`);
            testOracleExampleInst = inst;
            return oracleStorageInst.setOracleRegisterAddr(
                oracleRegisterInst.address,
                { from: oracleOwner },
            );
        })
        .then(() => {
            return oracleRegisterInst.registAddress(
                'OracleCore',
                oracleCoreInst.address,
                { from: oracleOwner },
            );
        })
        .then(() => {
            return oracleRegisterInst.registAddress(
                'OracleStorage',
                oracleStorageInst.address,
                { from: oracleOwner },
            );
        })
        .then(() => {
            return oracleRegisterInst.registAddress(
                'OracleWallet',
                oracleWalletInst.address,
                { from: oracleOwner },
            );
        })
        .then(() => {
            return oracleRegisterInst.registAddress(
                'OracleFeeWallet',
                oracleFeeWalletInst.address,
                { from: oracleOwner },
            );
        })
        .then(() => {
            return testRegisterInst.registAddress(
                'TestWalletDistributor',
                testWalletDistributorInst.address,
                { from: testOwner },
            );
        })
        .then(() => {
            return testRegisterInst.registAddress(
                'TestOracleExample',
                testOracleExampleInst.address,
                { from: testOwner },
            );
        })
        .then(() => {
            return testRegisterInst.registAddress(
                'TestStorage',
                testStorageInst.address,
                { from: testOwner },
            );
        })
        .then(() => {
            return testStorageInst.setAllower(
                testWalletDistributorInst.address,
                { from: testOwner },
            );
        })
        .then(() => {
            return testStorageInst.setAllower(
                testOracleExampleInst.address,
                { from: testOwner },
            );
        })
        .then(() => {
            return oracleFeeWalletInst.registerClientAddr(
                oracleWalletInst.address,
                { from: oracleOwner },
            );
        })
        .then(() => {
            console.log('Finish deploy');
        });
};
