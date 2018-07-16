pragma solidity 0.4.24;

contract OracleStorage {
    mapping(bytes32 => mapping(bytes32 => address)) private bytes32ToAddress;
    mapping(bytes32 => mapping(address => uint)) private addressToUint;

    address owner;
    address oracleCoreAddress;

    constructor (address _owner)
        public
    {
        owner = _owner;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    modifier onlyOwnerAndOracleCore {
        require(msg.sender == owner || msg.sender == oracleCoreAddress);
        _;
    }

    // Should be setup first.
    function setOracleCoreAddr (address _oracleCoreAddress)
        onlyOwner
        public
    {
        oracleCoreAddress = _oracleCoreAddress;
    }

    // bytes32ToAddress related function
    function delBytes32ToAddress(string _name, bytes32 _key)
        onlyOwnerAndOracleCore
        public
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        delete bytes32ToAddress[name][_key];
    }

    function setBytes32ToAddress(string _name, bytes32 _key, address _val)
        onlyOwnerAndOracleCore
        public
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        bytes32ToAddress[name][_key] = _val;
    }

    // Partial allow, allow everybody to get OracleAddress but other attribute is locked
    function getBytes32ToAddress(string _name, bytes32 _key)
        view
        public
        returns(address)
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        if (keccak256('OracleAddress') == name) {
            return bytes32ToAddress[name][_key];
        }
        require(msg.sender == owner || msg.sender == oracleCoreAddress);
        return bytes32ToAddress[name][_key];
    }


    // addressToUint related function
    function delAddressToUint(string _name, address _key)
        onlyOwnerAndOracleCore
        public
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        delete addressToUint[name][_key];
    }

    function setAddressToUint(string _name, address _key, uint _val)
        onlyOwnerAndOracleCore
        public
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        addressToUint[name][_key] = _val;
    }

    function getAddressToUint(string _name, address _key)
        onlyOwnerAndOracleCore
        view
        public
        returns(uint)
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        return addressToUint[name][_key];
    }
}
