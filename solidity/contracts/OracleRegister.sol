pragma solidity 0.4.24;

import {OracleStorage} from "./OracleStorage.sol";


contract OracleRegister {
    address owner;
    OracleStorage myStorage; 
    

    constructor (address _owner, address _storage) public {
        owner = _owner;
        myStorage = OracleStorage(_storage);
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    function registAddress(string _key, address _address)
        onlyOwner
        public
    {
       myStorage.setOracleAddress(_key, _address);
    }

    function getAddress(string _key)
        view
        public
        returns (address)
    {
       return myStorage.getOracleAddress(_key);
    }
}
