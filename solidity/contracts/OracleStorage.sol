pragma solidity 0.4.24;

contract OracleStorage {
    mapping(bytes32 => mapping(bytes32 => address)) private bytes32ToAddress;
    mapping(bytes32 => mapping(address => uint)) private addressToUint;
    mapping(bytes32 => bytes32[]) private bytes32Array;

    // bytes32ToAddress related function
    function delBytes32ToAddress(string _name, bytes32 _key)
        public
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        delete bytes32ToAddress[name][_key];
    }

    function setBytes32ToAddress(string _name, bytes32 _key, address _val)
        public
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        bytes32ToAddress[name][_key] = _val;
    }

    function getBytes32ToAddress(string _name, bytes32 _key)
        view
        public
        returns(address)
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        return bytes32ToAddress[name][_key];
    }



    // bytes32Array related function
    function getBytes32ArrayLength(string _name)
        view
        public
        returns(uint)
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        return bytes32Array[name].length;
    }

    function getBytes32ArrayEntry(string _name, uint _idx)
        view
        public
        returns(bytes32)
    {
        // only two contract can call this (and owner)
        require(getBytes32ArrayLength(_name) > _idx);

        bytes32 name = keccak256(abi.encodePacked(_name));
        return bytes32Array[name][_idx];
    }

    function setBytes32ArrayEntry(string _name, uint _idx, bytes32 _val)
        public
    {
        // only two contract can call this (and owner)
        require(getBytes32ArrayLength(_name) > _idx);
        bytes32 name = keccak256(abi.encodePacked(_name));
        bytes32Array[name][_idx] = _val;
    }

    function pushBytes32ArrayEntry(string _name, bytes32 _val)
        public
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        bytes32Array[name].push(_val);
    }

    function delBytes32ArrayEntry(string _name, uint _idx)
        public
    {
        // only two contract can call this (and owner)
        require(getBytes32ArrayLength(_name) > _idx);

        bytes32 name = keccak256(abi.encodePacked(_name));
        delete bytes32Array[name][_idx];
    }

    function delBytes32Array(string _name)
        public
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        delete bytes32Array[name];
    }

    function changeBytes32ArrayLength(string _name, uint _length)
        public
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        bytes32Array[name].length = _length;
    }


    // addressToUint related function
    function delAddressToUint(string _name, address _key)
        public
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        delete addressToUint[name][_key];
    }

    function setAddressToUint(string _name, address _key, uint _val)
        public
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        addressToUint[name][_key] = _val;
    }

    function getAddressToUint(string _name, address _key)
        view
        public
        returns(uint)
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        return addressToUint[name][_key];
    }
}
