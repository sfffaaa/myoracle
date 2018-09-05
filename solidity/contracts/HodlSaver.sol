pragma solidity 0.4.24;

import './SafeMath.sol';
import {HodlStorage} from "./HodlStorage.sol";
import {HodlRegister} from "./HodlRegister.sol";


contract HodlSaver {
    using SafeMath for uint256;
    address hodlRegisterAddr;
    address owner;

    event DepositBalance(address myAddress, uint threshold, uint nowValue, uint accuValue);
    event WithdrawBalance(address myAddress, uint threshold, uint value, uint price, bool transfered);
    
    constructor(address _owner, address _hodlRegisterAddr)
        public
    {
        owner = _owner;
        hodlRegisterAddr = _hodlRegisterAddr;
    }

    modifier OnlyAllowOwnerAndHodlOracle {
        address testOracleExampleAddr = HodlRegister(hodlRegisterAddr).getAddress('HodlOracle');
        require(0 != testOracleExampleAddr);
        require(msg.sender == owner || msg.sender == testOracleExampleAddr); 
        _;
    }

    function depositBalance(uint _threshold)
        payable
        public
    {
        address myHodlStorageAddr = HodlRegister(hodlRegisterAddr).getAddress('HodlStorage');
        assert(myHodlStorageAddr != 0);
        HodlStorage myStorage = HodlStorage(myHodlStorageAddr);

        address sender = msg.sender;
        require(0 != _threshold);
        uint indexA1 = myStorage.getBytes32AddressToUint('HodlSaverIndexA1', sender);
        uint threshold = myStorage.getBytes32AddressToUint('HodlSaverThreshold', sender);
        uint value = myStorage.getBytes32AddressToUint('HodlSaverValue', sender);

        if (indexA1 == 0) {
            indexA1 = myStorage.getBytes32AddressArrayLength('HodlSaverMyAddresses').add(1);
            threshold = _threshold;
            value = msg.value;
            myStorage.pushBytes32AddressArrayEntry('HodlSaverMyAddresses', sender);
        } else {
            threshold = _threshold;
            value = value.add(msg.value);
        }
        myStorage.setBytes32AddressToUint('HodlSaverIndexA1', sender, indexA1);
        myStorage.setBytes32AddressToUint('HodlSaverThreshold', sender, threshold);
        myStorage.setBytes32AddressToUint('HodlSaverValue', sender, value);

        emit DepositBalance(sender, _threshold, msg.value, value);
    }

    function withdrawBalance(uint _price)
        public
        OnlyAllowOwnerAndHodlOracle
    {
        address myHodlStorageAddr = HodlRegister(hodlRegisterAddr).getAddress('HodlStorage');
        assert(myHodlStorageAddr != 0);
        HodlStorage myStorage = HodlStorage(myHodlStorageAddr);

        uint myAddressesLength = myStorage.getBytes32AddressArrayLength('HodlSaverMyAddresses');
        for (uint i = 0; i < myAddressesLength; i++) {
            address hodlSaverAddress = myStorage.getBytes32AddressArrayEntry('HodlSaverMyAddresses', i);

            uint indexA1 = myStorage.getBytes32AddressToUint('HodlSaverIndexA1', hodlSaverAddress);
            uint threshold = myStorage.getBytes32AddressToUint('HodlSaverThreshold', hodlSaverAddress);
            uint value = myStorage.getBytes32AddressToUint('HodlSaverValue', hodlSaverAddress);
            if (0 == value || _price < threshold) {
                emit WithdrawBalance(hodlSaverAddress, threshold, value, _price, false);
                continue;
            }

            hodlSaverAddress.transfer(value);
            emit WithdrawBalance(hodlSaverAddress, threshold, value, _price, true);

            // Remove that data
            myStorage.setBytes32AddressToUint('HodlSaverIndexA1', hodlSaverAddress, indexA1);
            myStorage.setBytes32AddressToUint('HodlSaverThreshold', hodlSaverAddress, threshold);
            myStorage.setBytes32AddressToUint('HodlSaverValue', hodlSaverAddress, 0);
        }
    }
}
