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

    it('Action on addressArray checking', async () => {
        const ARRAY_TEST_KEYS = 'AddressArrayChecking';
        assert.equal(await oracleStorageInst.getAddressArrayLength(ARRAY_TEST_KEYS), 0,
            'There is no any array entry');

        oracleStorageInst.pushAddressArrayEntry(ARRAY_TEST_KEYS, 0x01);
        assert.equal(await oracleStorageInst.getAddressArrayLength(ARRAY_TEST_KEYS), 1,
            'Length should be the same');
        assert.equal(await oracleStorageInst.getAddressArrayEntry(ARRAY_TEST_KEYS, 0), 0x01,
            'Entry should be the same');

        await oracleStorageInst.setAddressArrayEntry(ARRAY_TEST_KEYS, 0, 0x02);
        assert.equal(await oracleStorageInst.getAddressArrayLength(ARRAY_TEST_KEYS), 1,
            'Length should be the same');
        assert.equal(await oracleStorageInst.getAddressArrayEntry(ARRAY_TEST_KEYS, 0), 0x02,
            'Entry should be the same');

        await oracleStorageInst.pushAddressArrayEntry(ARRAY_TEST_KEYS, 0x03);
        assert.equal(await oracleStorageInst.getAddressArrayLength(ARRAY_TEST_KEYS), 2,
            'Length should be the same');
        assert.equal(await oracleStorageInst.getAddressArrayEntry(ARRAY_TEST_KEYS, 0), 0x02,
            'Entry should be the same');
        assert.equal(await oracleStorageInst.getAddressArrayEntry(ARRAY_TEST_KEYS, 1), 0x03,
            'Entry should be the same');

        await oracleStorageInst.delAddressArrayEntry(ARRAY_TEST_KEYS, 0);
        assert.equal(await oracleStorageInst.getAddressArrayLength(ARRAY_TEST_KEYS), 2,
            'Length should be the same');
        assert.equal(await oracleStorageInst.getAddressArrayEntry(ARRAY_TEST_KEYS, 0), 0,
            'Entry should be the same');
        assert.equal(await oracleStorageInst.getAddressArrayEntry(ARRAY_TEST_KEYS, 1), 0x03,
            'Entry should be the same');

        await oracleStorageInst.changeAddressArrayLength(ARRAY_TEST_KEYS, 1);
        assert.equal(await oracleStorageInst.getAddressArrayLength(ARRAY_TEST_KEYS), 1,
            'Length should be the same');
        assert.equal(await oracleStorageInst.getAddressArrayEntry(ARRAY_TEST_KEYS, 0), 0,
            'Entry should be the same');

        await oracleStorageInst.delAddressArray(ARRAY_TEST_KEYS);
        assert.equal(await oracleStorageInst.getAddressArrayLength(ARRAY_TEST_KEYS), 0,
            'Length should be the same');
    });
});
