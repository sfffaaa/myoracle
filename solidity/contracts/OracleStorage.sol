pragma solidity 0.4.24;

contract OracleStorage {
    mapping(bytes32 => mapping(bytes32 => address)) private bytes32ToAddress;
    mapping(bytes32 => address[]) private addressArray;

    function delBytes32ToAddress(string _name, bytes32 _key)
        public
    {
        bytes32 name = keccak256(abi.encodePacked(_name));
        delete bytes32ToAddress[name][_key];
    }

    function setBytes32ToAddress(string _name, bytes32 _key, address _val)
        public
    {
        bytes32 name = keccak256(abi.encodePacked(_name));
        bytes32ToAddress[name][_key] = _val;
    }

    function getBytes32ToAddress(string _name, bytes32 _key)
        view
        public
        returns(address)
    {
        bytes32 name = keccak256(abi.encodePacked(_name));
        return bytes32ToAddress[name][_key];
    }



    function getAddressArrayLength(string _name)
        view
        public
        returns(uint)
    {
        bytes32 name = keccak256(abi.encodePacked(_name));
        return addressArray[name].length;
    }

    function getAddressArrayEntry(string _name, uint _idx)
        view
        public
        returns(address)
    {
        require(getAddressArrayLength(_name) > _idx);

        bytes32 name = keccak256(abi.encodePacked(_name));
        return addressArray[name][_idx];
    }

    function setAddressArrayEntry(string _name, uint _idx, address _val)
        public
    {
        require(getAddressArrayLength(_name) > _idx);
        bytes32 name = keccak256(abi.encodePacked(_name));
        addressArray[name][_idx] = _val;
    }

    function pushAddressArrayEntry(string _name, address _val)
        public
    {
        bytes32 name = keccak256(abi.encodePacked(_name));
        addressArray[name].push(_val);
    }

    function delAddressArrayEntry(string _name, uint _idx)
        public
    {
        require(getAddressArrayLength(_name) > _idx);

        bytes32 name = keccak256(abi.encodePacked(_name));
        delete addressArray[name][_idx];
    }

    function delAddressArray(string _name)
        public
    {
        bytes32 name = keccak256(abi.encodePacked(_name));
        delete addressArray[name];
    }

    function changeAddressArrayLength(string _name, uint _length)
        public
    {
        bytes32 name = keccak256(abi.encodePacked(_name));
        addressArray[name].length = _length;
    }
}
