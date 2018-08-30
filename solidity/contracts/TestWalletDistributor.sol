pragma solidity 0.4.24;

import './SafeMath.sol';
import {TestStorage} from "./TestStorage.sol";
import {OracleRegister} from "./OracleRegister.sol";


contract TestWalletDistributor {
    using SafeMath for uint256;
    address oracleRegisterAddr;

    event DepositBalance(address myAddress, uint threshold, uint nowValue, uint accuValue);
    event WithdrawBalance(address myAddress, uint threshold, uint value, uint price, bool transfered);
    
    constructor(address _oracleRegisterAddr)
        public
    {
        oracleRegisterAddr = _oracleRegisterAddr;
    }

    function depositBalance(uint _threshold)
        payable
        public
    {
        address myTestStorageAddr = OracleRegister(oracleRegisterAddr).getAddress('TestStorage');
        assert(myTestStorageAddr != 0);
        TestStorage myStorage = TestStorage(myTestStorageAddr);

        address sender = msg.sender;
        require(0 != _threshold);
        uint indexA1 = myStorage.getBytes32AddressToUint('TestWalletDistributorIndexA1', sender);
        uint threshold = myStorage.getBytes32AddressToUint('TestWalletDistributorThreshold', sender);
        uint value = myStorage.getBytes32AddressToUint('TestWalletDistributorValue', sender);

        if (indexA1 == 0) {
            indexA1 = myStorage.getBytes32AddressArrayLength('TestWalletDistributorMyAddresses').add(1);
            threshold = _threshold;
            value = msg.value;
            myStorage.pushBytes32AddressArrayEntry('TestWalletDistributorMyAddresses', sender);
        } else {
            threshold = _threshold;
            value = value.add(msg.value);
        }
        myStorage.setBytes32AddressToUint('TestWalletDistributorIndexA1', sender, indexA1);
        myStorage.setBytes32AddressToUint('TestWalletDistributorThreshold', sender, threshold);
        myStorage.setBytes32AddressToUint('TestWalletDistributorValue', sender, value);

        emit DepositBalance(sender, _threshold, msg.value, value);
    }

    function withdrawBalance(uint _price)
        public
    {
        address myTestStorageAddr = OracleRegister(oracleRegisterAddr).getAddress('TestStorage');
        assert(myTestStorageAddr != 0);
        TestStorage myStorage = TestStorage(myTestStorageAddr);

        uint myAddressesLength = myStorage.getBytes32AddressArrayLength('TestWalletDistributorMyAddresses');
        for (uint i = 0; i < myAddressesLength; i++) {
            address testAddress = myStorage.getBytes32AddressArrayEntry('TestWalletDistributorMyAddresses', i);

            uint indexA1 = myStorage.getBytes32AddressToUint('TestWalletDistributorIndexA1', testAddress);
            uint threshold = myStorage.getBytes32AddressToUint('TestWalletDistributorThreshold', testAddress);
            uint value = myStorage.getBytes32AddressToUint('TestWalletDistributorValue', testAddress);
            if (0 == value || _price < threshold) {
                emit WithdrawBalance(testAddress, threshold, value, _price, false);
                continue;
            }

            testAddress.transfer(value);
            emit WithdrawBalance(testAddress, threshold, value, _price, true);

            // Remove that data
            myStorage.setBytes32AddressToUint('TestWalletDistributorIndexA1', testAddress, indexA1);
            myStorage.setBytes32AddressToUint('TestWalletDistributorThreshold', testAddress, threshold);
            myStorage.setBytes32AddressToUint('TestWalletDistributorValue', testAddress, 0);
        }
    }
}
