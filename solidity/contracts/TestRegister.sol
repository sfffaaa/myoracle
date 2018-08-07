pragma solidity 0.4.24;

import {TestStorage} from "./TestStorage.sol";

// [TODO] Not use right now, USE OracleRegister right now
contract TestRegister {
    address owner;
    TestStorage myStorage; 
    

    constructor (address _owner, address _storage) public {
        owner = _owner;
        myStorage = TestStorage(_storage);
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    function registAddress(string _key, address _address)
        onlyOwner
        public
    {
       myStorage.setAddress(_key, _address);
    }

    function getAddress(string _key)
        view
        public
        returns (address)
    {
       return myStorage.getAddress(_key);
    }
}
