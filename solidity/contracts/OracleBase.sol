pragma solidity 0.4.24;

import {OracleRegister} from "./OracleRegister.sol";
import {OracleCore} from "./OracleCore.sol";

// OracleBase and its childs need deploy after oracleCore and OracleStorage.
contract OracleBase {
   
    address myRegisterAddr;
    address owner;

    //[TODO] Need use register instead of real storage address
    constructor (address _owner, address _oracleRegisterAddr)
        public
    {
        require(_owner != 0);
        require(_oracleRegisterAddr != 0);
        owner = _owner;
        myRegisterAddr = _oracleRegisterAddr;
    }

    modifier onlyOwnerAndMyself {
        require(msg.sender == address(this) || msg.sender == owner);
        _;
    }

    modifier onlyOwnerAndOracleCore {
        address oracleCoreAddress = OracleRegister(myRegisterAddr).getAddress('OracleCore');
        require(oracleCoreAddress != 0);
        require(msg.sender == owner || msg.sender == oracleCoreAddress);
        _;
    }

    function __querySentNode(string _requests)
        public
        onlyOwnerAndMyself
        returns (bytes32)
    {
        // only self and owner can call this
        address oracleCoreAddress = OracleRegister(myRegisterAddr).getAddress('OracleCore');
        require(oracleCoreAddress != 0);

        return OracleCore(oracleCoreAddress).querySentNode(this, _requests);
    }

    function __callback(bytes32 _queryId, string _response, bytes32 _hash) public;
}
