/* global artifacts, contract, it, assert, before */

const OracleStorage = artifacts.require('OracleStorage');

contract('OracleStorageBasic', (accounts) => {
    const TEST_STORAGE_NAME = 'TestMyName';
    let oracleStorageInst = null;
    const oracleOwner = accounts[1];

    before(async () => {
        oracleStorageInst = await OracleStorage.deployed();
    });

    // Bytes32ToAddress related test
    it('Get/Set/Delete Bytes32ToAddress checking', async () => {
        await oracleStorageInst.setBytes32ToAddress(
            TEST_STORAGE_NAME,
            'key',
            oracleStorageInst.address,
            { from: oracleOwner },
        );
        let myAddress = await oracleStorageInst.getBytes32ToAddress(
            TEST_STORAGE_NAME,
            'key',
            { from: oracleOwner },
        );
        assert.equal(myAddress, oracleStorageInst.address, 'Two address should be the same');
        await oracleStorageInst.delBytes32ToAddress(
            TEST_STORAGE_NAME,
            'key',
            { from: oracleOwner },
        );
        myAddress = await oracleStorageInst.getBytes32ToAddress(
            TEST_STORAGE_NAME,
            'key',
            { from: oracleOwner },
        );
        assert.equal(myAddress, 0, 'Two address should be the same');
    });

    it('Get none exist name', async () => {
        const myAddress = await oracleStorageInst.getBytes32ToAddress(
            'NON_EXIST',
            'key',
            { from: oracleOwner },
        );
        assert.equal(myAddress, 0, 'Two address should be the same');
    });

    it('Get none exist key', async () => {
        await oracleStorageInst.setBytes32ToAddress(
            'NON_EXIST',
            'key',
            oracleStorageInst.address,
            { from: oracleOwner },
        );
        const myAddress = await oracleStorageInst.getBytes32ToAddress(
            'NON_EXIST',
            'no exist',
            { from: oracleOwner },
        );
        assert.equal(myAddress, 0, 'Two address should be the same');
    });


    it('delete none exist name', async () => {
        await oracleStorageInst.delBytes32ToAddress(
            'NON_EXIST_2',
            'key',
            { from: oracleOwner },
        );
        const myAddress = await oracleStorageInst.getBytes32ToAddress(
            'NON_EXIST_2',
            'key',
            { from: oracleOwner },
        );
        assert.equal(myAddress, 0, 'Two address should be the same');
    });

    // addressToUint related test
    it('Get/Set/Delete addressToUint checking', async () => {
        await oracleStorageInst.setAddressToUint(
            TEST_STORAGE_NAME,
            0x01,
            2,
            { from: oracleOwner },
        );
        let addressUint = await oracleStorageInst.getAddressToUint(
            TEST_STORAGE_NAME,
            0x01,
            { from: oracleOwner },
        );
        assert.equal(2, addressUint, 'Two uint return should be the same');
        await oracleStorageInst.delAddressToUint(
            TEST_STORAGE_NAME,
            0x01,
            { from: oracleOwner },
        );
        addressUint = await oracleStorageInst.getAddressToUint(
            TEST_STORAGE_NAME,
            0x01,
            { from: oracleOwner },
        );
        assert.equal(addressUint, 0, 'Two address should be the same');
    });
});
