pragma solidity 0.4.24;

import {OracleBase} from "./OracleBase.sol";
import {OracleStorage} from "./OracleStorage.sol";

contract TestOracleExample is OracleBase {
    event ShowCallback(bytes32 queryId, bytes32 hash, string response);

    constructor (address _oracleStorage) OracleBase( _oracleStorage)
        public
    {}

    function querySentNode()
        public
    {
        bytes32 queryId = __querySentNode('Just for test');
        OracleStorage(myStorageAddr).pushBytes32ArrayEntry('TestOracleExampleQueryIds', queryId);
    }

    // [TODO] We should have permission restriction
    function __callback(bytes32 _queryId, bytes32 _hash, string _response)
        public
    {
        emit ShowCallback(_queryId, _hash, _response);
    }
}
