pragma solidity 0.4.24;

import {OracleStorage} from "./OracleStorage.sol";
import {OracleCore} from "./OracleCore.sol";

// OracleBase and its childs need deploy after oracleCore and OracleStorage.
contract OracleBase {
   
    address myStorageAddr;

    constructor (address _oracleStorageAddr)
        public
    {
        require(_oracleStorageAddr != 0);
        myStorageAddr = _oracleStorageAddr;
    }

    function querySentNode(string _requests)
        public
    {
        address oracleCoreAddress = OracleStorage(myStorageAddr).getBytes32ToAddress('OracleAddress', 'OracleCore');
        require(oracleCoreAddress != 0);

        OracleCore(oracleCoreAddress).querySentNode(this, _requests);
    }

    function __callback(bytes32 _queryId, bytes32 _hash, string _response) public;
}
