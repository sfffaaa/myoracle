/* global artifacts */

const OracleRegister = artifacts.require('./OracleRegister');
const OracleStorage = artifacts.require('./OracleStorage');
const OracleCore = artifacts.require('./OracleCore');
const OracleWallet = artifacts.require('./OracleWallet');
const OracleFeeWallet = artifacts.require('./OracleFeeWallet');

const HodlStorage = artifacts.require('./HodlStorage');
const HodlSaver = artifacts.require('./HodlSaver');
const HodlRegister = artifacts.require('./HodlRegister');
const HodlOracle = artifacts.require('./HodlOracle');


module.exports = (deployer, network, accounts) => {
    let oracleStorageInst = null;
    let oracleCoreInst = null;
    let oracleRegisterInst = null;
    let oracleWalletInst = null;
    let oracleFeeWalletInst = null;

    let hodlStorageInst = null;
    let hodlSaverInst = null;
    let hodlOracleInst = null;
    let hodlRegisterInst = null;

    const oracleOwner = accounts[1];
    const hodlOwner = accounts[2];

    deployer.deploy(HodlStorage, hodlOwner).then((inst) => {
        console.log(`HodlStorage address: ${inst.address}`);
        hodlStorageInst = inst;
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
                oracleRegisterInst.address,
            );
        })
        .then((inst) => {
            console.log(`OracleFeeWallet address: ${inst.address}`);
            oracleFeeWalletInst = inst;
            return deployer.deploy(
                HodlRegister,
                hodlOwner,
            );
        })
        .then((inst) => {
            console.log(`HodlRegister address: ${inst.address}`);
            hodlRegisterInst = inst;
            return deployer.deploy(
                HodlSaver,
                hodlOwner,
                hodlRegisterInst.address,
            );
        })
        .then((inst) => {
            console.log(`HodlSaver address: ${inst.address}`);
            hodlSaverInst = inst;
            return deployer.deploy(
                HodlOracle,
                hodlOwner,
                oracleRegisterInst.address,
                hodlRegisterInst.address,
            );
        })
        .then((inst) => {
            console.log(`HodlOracle address: ${inst.address}`);
            hodlOracleInst = inst;
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
            return hodlRegisterInst.registAddress(
                'HodlSaver',
                hodlSaverInst.address,
                { from: hodlOwner },
            );
        })
        .then(() => {
            return hodlRegisterInst.registAddress(
                'HodlOracle',
                hodlOracleInst.address,
                { from: hodlOwner },
            );
        })
        .then(() => {
            return hodlRegisterInst.registAddress(
                'HodlStorage',
                hodlStorageInst.address,
                { from: hodlOwner },
            );
        })
        .then(() => {
            return hodlStorageInst.setAllower(
                hodlSaverInst.address,
                { from: hodlOwner },
            );
        })
        .then(() => {
            return hodlStorageInst.setAllower(
                hodlOracleInst.address,
                { from: hodlOwner },
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
