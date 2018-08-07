/* global artifacts, contract, it, assert, before */

const TestStorage = artifacts.require('TestStorage');

contract('TestStorageBasic', () => {
    let testStorageInst = null;

    before(async () => {
        testStorageInst = await TestStorage.deployed();
    });

    // Bytes32Array related test
    it('Action on addressArray checking', async () => {
        const ARRAY_TEST_KEYS = 'Bytes32ArrayChecking';
        assert.equal(await testStorageInst.getBytes32ArrayLength(ARRAY_TEST_KEYS), 0,
            'There is no any array entry');

        testStorageInst.pushBytes32ArrayEntry(ARRAY_TEST_KEYS,
            '0x0000000000000000000000000000000000000000000000000000000000000001');
        assert.equal(await testStorageInst.getBytes32ArrayLength(ARRAY_TEST_KEYS), 1,
            'Length should be the same');
        assert.equal(await testStorageInst.getBytes32ArrayEntry(ARRAY_TEST_KEYS, 0),
            '0x0000000000000000000000000000000000000000000000000000000000000001',
            'Entry should be the same');

        await testStorageInst.setBytes32ArrayEntry(ARRAY_TEST_KEYS, 0,
            '0x2000000000000000000000000000000000000000000000000000000000000000');
        assert.equal(await testStorageInst.getBytes32ArrayLength(ARRAY_TEST_KEYS), 1,
            'Length should be the same');
        assert.equal(await testStorageInst.getBytes32ArrayEntry(ARRAY_TEST_KEYS, 0),
            '0x2000000000000000000000000000000000000000000000000000000000000000',
            'Entry should be the same');

        await testStorageInst.pushBytes32ArrayEntry(ARRAY_TEST_KEYS,
            '0x3000000000000000000000000000000000000000000000000000000000000000');
        assert.equal(await testStorageInst.getBytes32ArrayLength(ARRAY_TEST_KEYS), 2,
            'Length should be the same');
        assert.equal(await testStorageInst.getBytes32ArrayEntry(ARRAY_TEST_KEYS, 0),
            '0x2000000000000000000000000000000000000000000000000000000000000000',
            'Entry should be the same');
        assert.equal(await testStorageInst.getBytes32ArrayEntry(ARRAY_TEST_KEYS, 1),
            '0x3000000000000000000000000000000000000000000000000000000000000000',
            'Entry should be the same');

        await testStorageInst.delBytes32ArrayEntry(ARRAY_TEST_KEYS, 0);
        assert.equal(await testStorageInst.getBytes32ArrayLength(ARRAY_TEST_KEYS), 2,
            'Length should be the same');
        assert.equal(await testStorageInst.getBytes32ArrayEntry(ARRAY_TEST_KEYS, 0), 0,
            'Entry should be the same');
        assert.equal(await testStorageInst.getBytes32ArrayEntry(ARRAY_TEST_KEYS, 1),
            '0x3000000000000000000000000000000000000000000000000000000000000000',
            'Entry should be the same');

        await testStorageInst.changeBytes32ArrayLength(ARRAY_TEST_KEYS, 1);
        assert.equal(await testStorageInst.getBytes32ArrayLength(ARRAY_TEST_KEYS), 1,
            'Length should be the same');
        assert.equal(await testStorageInst.getBytes32ArrayEntry(ARRAY_TEST_KEYS, 0), 0,
            'Entry should be the same');

        await testStorageInst.delBytes32Array(ARRAY_TEST_KEYS);
        assert.equal(await testStorageInst.getBytes32ArrayLength(ARRAY_TEST_KEYS), 0,
            'Length should be the same');
    });
    // bytes32AddressMap related test
    it('Action on bytes32AddressMap checking', async () => {
        const ADDRESS_MAP_KEY = 'show me the money';
        assert.equal(
            await testStorageInst.getAddress(ADDRESS_MAP_KEY),
            0,
            'There no address here',
        );
        await testStorageInst.setAddress(ADDRESS_MAP_KEY, testStorageInst.address);
        assert.equal(
            await testStorageInst.getAddress(ADDRESS_MAP_KEY),
            testStorageInst.address,
            'Address should be the same',
        );
        await testStorageInst.setAddress(ADDRESS_MAP_KEY, 1);
        assert.equal(
            await testStorageInst.getAddress(ADDRESS_MAP_KEY),
            1,
            'Address should be the same',
        );
    });
});
