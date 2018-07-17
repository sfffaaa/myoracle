/* global artifacts, contract, it, assert */

const OracleRegister = artifacts.require('OracleRegister');


contract('OracleRegister', (accounts) => {
    it('Basic test', async () => {
        const oracleRegisterInst = await OracleRegister.deployed();
        let myAddress = await oracleRegisterInst.getAddress('Why so serious');
        assert.equal(0, myAddress, 'Two object should be the same');

        await oracleRegisterInst.registAddress('Why so serious', accounts[1]);

        myAddress = await oracleRegisterInst.getAddress('Why so serious');
        assert.equal(accounts[1], myAddress, 'Two object should be the same');
    });
});
