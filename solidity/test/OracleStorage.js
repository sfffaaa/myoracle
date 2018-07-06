/* global artifacts, contract, it, assert, before */

const OracleStorage = artifacts.require('OracleStorage');

contract('OracleStorageBasic', () => {
    const TEST_STORAGE_NAME = 'TestMyName';
    let oracleStorageInst = null;

    before(async () => {
        oracleStorageInst = await OracleStorage.deployed();
    });

    it('Get/Set/Delete checking', async () => {
        await oracleStorageInst.setBytes32ToAddress(TEST_STORAGE_NAME, 'key', oracleStorageInst.address);
        let myAddress = await oracleStorageInst.getBytes32ToAddress(TEST_STORAGE_NAME, 'key');
        assert.equal(myAddress, oracleStorageInst.address, 'Two address should be the same');
        await oracleStorageInst.delBytes32ToAddress(TEST_STORAGE_NAME, 'key');
        myAddress = await oracleStorageInst.getBytes32ToAddress(TEST_STORAGE_NAME, 'key');
        assert.equal(myAddress, 0, 'Two address should be the same');
    });

    it('Get none exist name', async () => {
        const myAddress = await oracleStorageInst.getBytes32ToAddress('NON_EXIST', 'key');
        assert.equal(myAddress, 0, 'Two address should be the same');
    });

    it('Get none exist key', async () => {
        await oracleStorageInst.setBytes32ToAddress('NON_EXIST', 'key', oracleStorageInst.address);
        const myAddress = await oracleStorageInst.getBytes32ToAddress('NON_EXIST', 'no exist');
        assert.equal(myAddress, 0, 'Two address should be the same');
    });


    it('delete none exist name', async () => {
        await oracleStorageInst.delBytes32ToAddress('NON_EXIST_2', 'key');
        const myAddress = await oracleStorageInst.getBytes32ToAddress('NON_EXIST_2', 'key');
        assert.equal(myAddress, 0, 'Two address should be the same');
    });
});
