pragma solidity 0.4.24;


contract HodlRegister {
    address owner;
    mapping (string => address) stringAddressMap;
    

    constructor (address _owner) public {
        owner = _owner;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    function registAddress(string _key, address _address)
        onlyOwner
        external
    {
        stringAddressMap[_key] = _address;
    }

    function getAddress(string _key)
        view
        external
        returns (address)
    {
       return stringAddressMap[_key];
    }
}
