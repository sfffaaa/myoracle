pragma solidity 0.4.24;

contract TestStorage {
    mapping(bytes32 => bytes32[]) private bytes32Array;
    mapping(bytes32 => address) private bytes32AddressMap;
    mapping(bytes32 => mapping(address => uint)) private bytes32AddressToUint;
    mapping(bytes32 => address[]) private bytes32AddressArray;

    address owner;
    address[] allowers;

    constructor (address _owner)
        public
    {
        require(_owner != address(0));
        owner = _owner;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    modifier allowOnwerAndAllower {
        if (msg.sender == owner) {
            _;
            return;
        }
        for (uint i = 0; i < allowers.length; i++) {
            if (msg.sender == allowers[i]) {
                _;
                return;
            }
        }
        require(false);
    }

    function setAllower(address _allower)
        public
        onlyOwner
    {
        require(_allower != address(0));
        allowers.push(_allower);
    }

    function getBytes32AddressToUint(string _name, address _addr)
        view
        public
        allowOnwerAndAllower
        returns(uint)
    {
        bytes32 name = keccak256(abi.encodePacked(_name));
        return bytes32AddressToUint[name][_addr];
    }

    function setBytes32AddressToUint(string _name, address _addr, uint _value)
        public
        allowOnwerAndAllower
    {
        bytes32 name = keccak256(abi.encodePacked(_name));
        bytes32AddressToUint[name][_addr] = _value;
    }

    // bytes32Array related function
    function getBytes32AddressArrayLength(string _name)
        view
        public
        allowOnwerAndAllower
        returns(uint)
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        return bytes32AddressArray[name].length;
    }

    function getBytes32AddressArrayEntry(string _name, uint _idx)
        view
        public
        allowOnwerAndAllower
        returns(address)
    {
        // only two contract can call this (and owner)
        require(getBytes32AddressArrayLength(_name) > _idx);

        bytes32 name = keccak256(abi.encodePacked(_name));
        return bytes32AddressArray[name][_idx];
    }

    function setBytes32AddressArrayEntry(string _name, uint _idx, address  _val)
        public
        allowOnwerAndAllower
    {
        // only two contract can call this (and owner)
        require(getBytes32AddressArrayLength(_name) > _idx);
        bytes32 name = keccak256(abi.encodePacked(_name));
        bytes32AddressArray[name][_idx] = _val;
    }

    function pushBytes32AddressArrayEntry(string _name, address _val)
        public
        allowOnwerAndAllower
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        bytes32AddressArray[name].push(_val);
    }

    function delBytes32AddressArrayEntry(string _name, uint _idx)
        public
        allowOnwerAndAllower
    {
        // only two contract can call this (and owner)
        require(getBytes32ArrayLength(_name) > _idx);

        bytes32 name = keccak256(abi.encodePacked(_name));
        delete bytes32AddressArray[name][_idx];
    }

    function delBytes32AddressArray(string _name)
        public
        allowOnwerAndAllower
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        delete bytes32AddressArray[name];
    }

    function changeBytes32AddressArrayLength(string _name, uint _length)
        public
        allowOnwerAndAllower
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        bytes32AddressArray[name].length = _length;
    }


    // bytes32Array related function
    function getBytes32ArrayLength(string _name)
        view
        public
        allowOnwerAndAllower
        returns(uint)
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        return bytes32Array[name].length;
    }

    function getBytes32ArrayEntry(string _name, uint _idx)
        view
        public
        allowOnwerAndAllower
        returns(bytes32)
    {
        // only two contract can call this (and owner)
        require(getBytes32ArrayLength(_name) > _idx);

        bytes32 name = keccak256(abi.encodePacked(_name));
        return bytes32Array[name][_idx];
    }

    function setBytes32ArrayEntry(string _name, uint _idx, bytes32 _val)
        public
        allowOnwerAndAllower
    {
        // only two contract can call this (and owner)
        require(getBytes32ArrayLength(_name) > _idx);
        bytes32 name = keccak256(abi.encodePacked(_name));
        bytes32Array[name][_idx] = _val;
    }

    function pushBytes32ArrayEntry(string _name, bytes32 _val)
        public
        allowOnwerAndAllower
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        bytes32Array[name].push(_val);
    }

    function delBytes32ArrayEntry(string _name, uint _idx)
        public
        allowOnwerAndAllower
    {
        // only two contract can call this (and owner)
        require(getBytes32ArrayLength(_name) > _idx);

        bytes32 name = keccak256(abi.encodePacked(_name));
        delete bytes32Array[name][_idx];
    }

    function delBytes32Array(string _name)
        public
        allowOnwerAndAllower
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        delete bytes32Array[name];
    }

    function changeBytes32ArrayLength(string _name, uint _length)
        public
        allowOnwerAndAllower
    {
        // only two contract can call this (and owner)
        bytes32 name = keccak256(abi.encodePacked(_name));
        bytes32Array[name].length = _length;
    }
}
