/* global artifacts, contract, it, assert, before */

const HodlStorage = artifacts.require('HodlStorage');

contract('HodlStorageBasic', (accounts) => {
    let hodlStorageInst = null;
    const testOwner = accounts[2];

    before(async () => {
        hodlStorageInst = await HodlStorage.deployed();
    });

    // Bytes32Array related test
    it('Action on addressArray checking', async () => {
        const ARRAY_TEST_KEYS = 'Bytes32ArrayChecking';
        let length = await hodlStorageInst.getBytes32ArrayLength(
            ARRAY_TEST_KEYS,
            { from: testOwner },
        );
        assert.equal(
            length,
            0,
            'There is no any array entry',
        );

        hodlStorageInst.pushBytes32ArrayEntry(
            ARRAY_TEST_KEYS,
            '0x0000000000000000000000000000000000000000000000000000000000000001',
            { from: testOwner },
        );

        length = await hodlStorageInst.getBytes32ArrayLength(
            ARRAY_TEST_KEYS,
            { from: testOwner },
        );
        assert.equal(length, 1,
            'Length should be the same');
        let checkEntry = await hodlStorageInst.getBytes32ArrayEntry(
            ARRAY_TEST_KEYS,
            0,
            { from: testOwner },
        );
        assert.equal(
            checkEntry,
            '0x0000000000000000000000000000000000000000000000000000000000000001',
            'Entry should be the same',
        );

        await hodlStorageInst.setBytes32ArrayEntry(
            ARRAY_TEST_KEYS,
            0,
            '0x2000000000000000000000000000000000000000000000000000000000000000',
            { from: testOwner },
        );
        length = await hodlStorageInst.getBytes32ArrayLength(
            ARRAY_TEST_KEYS,
            { from: testOwner },
        );
        assert.equal(length, 1, 'Length should be the same');
        checkEntry = await hodlStorageInst.getBytes32ArrayEntry(
            ARRAY_TEST_KEYS,
            0,
            { from: testOwner },
        );
        assert.equal(
            checkEntry,
            '0x2000000000000000000000000000000000000000000000000000000000000000',
            'Entry should be the same',
        );

        await hodlStorageInst.pushBytes32ArrayEntry(
            ARRAY_TEST_KEYS,
            '0x3000000000000000000000000000000000000000000000000000000000000000',
            { from: testOwner },
        );
        length = await hodlStorageInst.getBytes32ArrayLength(
            ARRAY_TEST_KEYS,
            { from: testOwner },
        );
        assert.equal(length, 2, 'Length should be the same');
        checkEntry = await hodlStorageInst.getBytes32ArrayEntry(
            ARRAY_TEST_KEYS,
            0,
            { from: testOwner },
        );
        assert.equal(
            checkEntry,
            '0x2000000000000000000000000000000000000000000000000000000000000000',
            'Entry should be the same',
        );
        checkEntry = await hodlStorageInst.getBytes32ArrayEntry(
            ARRAY_TEST_KEYS,
            1,
            { from: testOwner },
        );
        assert.equal(
            checkEntry,
            '0x3000000000000000000000000000000000000000000000000000000000000000',
            'Entry should be the same',
        );

        await hodlStorageInst.delBytes32ArrayEntry(
            ARRAY_TEST_KEYS,
            0,
            { from: testOwner },
        );
        length = await hodlStorageInst.getBytes32ArrayLength(
            ARRAY_TEST_KEYS,
            { from: testOwner },
        );
        assert.equal(length, 2, 'Length should be the same');
        checkEntry = await hodlStorageInst.getBytes32ArrayEntry(
            ARRAY_TEST_KEYS,
            0,
            { from: testOwner },
        );
        assert.equal(checkEntry, 0, 'Entry should be the same');
        checkEntry = await hodlStorageInst.getBytes32ArrayEntry(
            ARRAY_TEST_KEYS,
            1,
            { from: testOwner },
        );
        assert.equal(
            checkEntry,
            '0x3000000000000000000000000000000000000000000000000000000000000000',
            'Entry should be the same',
        );

        await hodlStorageInst.changeBytes32ArrayLength(
            ARRAY_TEST_KEYS,
            1,
            { from: testOwner },
        );
        length = await hodlStorageInst.getBytes32ArrayLength(
            ARRAY_TEST_KEYS,
            { from: testOwner },
        );
        assert.equal(length, 1, 'Length should be the same');
        checkEntry = await hodlStorageInst.getBytes32ArrayEntry(
            ARRAY_TEST_KEYS,
            0,
            { from: testOwner },
        );
        assert.equal(checkEntry, 0, 'Entry should be the same');

        await hodlStorageInst.delBytes32Array(
            ARRAY_TEST_KEYS,
            { from: testOwner },
        );
        length = await hodlStorageInst.getBytes32ArrayLength(
            ARRAY_TEST_KEYS,
            { from: testOwner },
        );
        assert.equal(length, 0, 'Length should be the same');
    });
});
