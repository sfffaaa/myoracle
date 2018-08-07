pragma solidity 0.4.24;

contract TestStorage {
    mapping(bytes32 => bytes32[]) private bytes32Array;
    mapping(bytes32 => address) private bytes32AddressMap;

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

    // [TODO] No use here, because we use OracleRegister right now.
    function setAddress(string _key, address _addr)
        public
    {
        bytes32 name = keccak256(abi.encodePacked(_key));
        bytes32AddressMap[name] = _addr;
    }

    function getAddress(string _key)
        view
        public
        returns (address)
    {
        bytes32 name = keccak256(abi.encodePacked(_key));
        return bytes32AddressMap[name];
    }
}
