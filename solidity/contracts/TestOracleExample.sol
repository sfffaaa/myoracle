pragma solidity 0.4.24;

import {OracleBase} from "./OracleBase.sol";
import {OracleStorage} from "./OracleStorage.sol";

contract TestOracleExample is OracleBase {
    event SentCallback(bytes32 queryId, string data);
    event ShowCallback(bytes32 queryId, bytes32 hash, string response);

    constructor (address _oracleStorage) OracleBase( _oracleStorage)
        public
    {}

    function querySentNode(string _data)
        public
    {
        bytes32 queryId = __querySentNode(_data);
        OracleStorage(myStorageAddr).pushBytes32ArrayEntry('TestOracleExampleQueryIds', queryId);
        emit SentCallback(queryId, _data);
    }

    function getLastestQueryId()
        view
        public
        returns (bytes32)
    {
        uint queryIdsLength = OracleStorage(myStorageAddr).getBytes32ArrayLength('TestOracleExampleQueryIds');
        require(queryIdsLength > 0);
        return OracleStorage(myStorageAddr).getBytes32ArrayEntry('TestOracleExampleQueryIds', queryIdsLength - 1);
    }

    // [TODO] We should have permission restriction
    function __callback(bytes32 _queryId, bytes32 _hash, string _response)
        public
    {
        emit ShowCallback(_queryId, _hash, _response);
    }
}
