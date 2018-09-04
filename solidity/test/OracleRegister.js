/* global artifacts, contract, it, assert */

const OracleRegister = artifacts.require('OracleRegister');


contract('OracleRegister', (accounts) => {
    const oracleOwner = accounts[1];
    const otherUser = accounts[3];

    it('Basic test', async () => {
        const oracleRegisterInst = await OracleRegister.deployed();
        let myAddress = await oracleRegisterInst.getAddress(
            'Why so serious',
            { from: otherUser },
        );
        assert.equal(0, myAddress, 'Two object should be the same');

        await oracleRegisterInst.registAddress(
            'Why so serious',
            accounts[1],
            { from: oracleOwner },
        );

        myAddress = await oracleRegisterInst.getAddress(
            'Why so serious',
            { from: otherUser },
        );
        assert.equal(accounts[1], myAddress, 'Two object should be the same');
    });
});
