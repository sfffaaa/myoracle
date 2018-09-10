pragma solidity 0.4.24;

import {OracleConstant} from "./OracleConstant.sol";
import {OracleRegister} from "./OracleRegister.sol";

contract OracleStorage is OracleConstant {
    mapping(bytes32 => mapping(bytes32 => address)) private bytes32ToAddress;
    mapping(bytes32 => mapping(address => uint)) private addressToUint;
    mapping(bytes32 => address[]) private bytes32AddressArray;

    address owner;
    address oracleRegisterAddr;

    constructor (address _owner)
        public
    {
        owner = _owner;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    modifier onlyOwnerAndOracleCoreAndFeeWallet {
        require(msg.sender == owner ||
                msg.sender == OracleRegister(oracleRegisterAddr).getAddress(ORACLE_CORE_ADDR_KEY) ||
                msg.sender == OracleRegister(oracleRegisterAddr).getAddress(ORACLE_FEE_WALLET_ADDR_KEY));
        _;
    }

    modifier onlyOwnerAndOracleRegister {
        require(msg.sender == owner || msg.sender == oracleRegisterAddr);
        _;
    }

    function setOracleRegisterAddr(address _oracleRegisterAddr)
        onlyOwner
        external
    {
        oracleRegisterAddr = _oracleRegisterAddr;
    }

    // bytes32ToAddress related function
    function delBytes32ToAddress(string _name, bytes32 _key)
        onlyOwnerAndOracleCoreAndFeeWallet
        external
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        delete bytes32ToAddress[name][_key];
    }

    function setBytes32ToAddress(string _name, bytes32 _key, address _val)
        onlyOwnerAndOracleCoreAndFeeWallet
        external
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        bytes32ToAddress[name][_key] = _val;
    }

    // Partial allow, allow everybody to get OracleAddress but other attribute is locked
    function getBytes32ToAddress(string _name, bytes32 _key)
        onlyOwnerAndOracleCoreAndFeeWallet
        view
        external
        returns(address)
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        return bytes32ToAddress[name][_key];
    }

    // addressToUint related function
    function delAddressToUint(string _name, address _key)
        onlyOwnerAndOracleCoreAndFeeWallet
        external
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        delete addressToUint[name][_key];
    }

    function setAddressToUint(string _name, address _key, uint _val)
        onlyOwnerAndOracleCoreAndFeeWallet
        external
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        addressToUint[name][_key] = _val;
    }

    function getAddressToUint(string _name, address _key)
        onlyOwnerAndOracleCoreAndFeeWallet
        view
        external
        returns(uint)
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        return addressToUint[name][_key];
    }


    // bytes32Array related function
    function getBytes32AddressArrayLength(string _name)
        view
        public
        onlyOwnerAndOracleCoreAndFeeWallet
        returns(uint)
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        return bytes32AddressArray[name].length;
    }

    function getBytes32AddressArrayEntry(string _name, uint _idx)
        view
        external
        onlyOwnerAndOracleCoreAndFeeWallet
        returns(address)
    {
        // only two contract can call this (and owner)
        require(getBytes32AddressArrayLength(_name) > _idx);

        bytes32 name = keccak256(abi.encodePacked(_name));
        return bytes32AddressArray[name][_idx];
    }

    function setBytes32AddressArrayEntry(string _name, uint _idx, address  _val)
        external
        onlyOwnerAndOracleCoreAndFeeWallet
    {
        // only two contract can call this (and owner)
        require(getBytes32AddressArrayLength(_name) > _idx);
        bytes32 name = keccak256(abi.encodePacked(_name));
        bytes32AddressArray[name][_idx] = _val;
    }

    function pushBytes32AddressArrayEntry(string _name, address _val)
        external
        onlyOwnerAndOracleCoreAndFeeWallet
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        bytes32AddressArray[name].push(_val);
    }

    function delBytes32AddressArrayEntry(string _name, uint _idx)
        external
        onlyOwnerAndOracleCoreAndFeeWallet
    {
        // only two contract can call this (and owner)
        require(getBytes32AddressArrayLength(_name) > _idx);

        bytes32 name = keccak256(abi.encodePacked(_name));
        delete bytes32AddressArray[name][_idx];
    }

    function delBytes32AddressArray(string _name)
        external
        onlyOwnerAndOracleCoreAndFeeWallet
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        delete bytes32AddressArray[name];
    }

    function changeBytes32AddressArrayLength(string _name, uint _length)
        external
        onlyOwnerAndOracleCoreAndFeeWallet
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        bytes32AddressArray[name].length = _length;
    }
}
