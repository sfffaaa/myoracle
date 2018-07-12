pragma solidity 0.4.24;

import {OracleBase} from "./OracleBase.sol";
import {OracleStorage} from "./OracleStorage.sol";

contract TestOracleExample is OracleBase {
    event SentCallback(bytes32 queryId, string request);
    event ShowCallback(bytes32 queryId, string response, bytes32 hash);

    constructor (address _oracleStorage) OracleBase( _oracleStorage)
        public
    {}

    function trigger()
        public
    {
        string memory request = 'json(https://api.kraken.com/0/public/Ticker?pair=ETHUSD)["result"]["XETHZUSD"]["c"]["0"]';
        querySentNode(request);
    }

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
    function __callback(bytes32 _queryId, string _response, bytes32 _hash)
        public
    {
        emit ShowCallback(_queryId, _response, _hash);
    }
}
