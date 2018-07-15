pragma solidity 0.4.24;

import {OracleBase} from "./OracleBase.sol";
import {OracleStorage} from "./OracleStorage.sol";
import {TestStorage} from "./TestStorage.sol";

contract TestOracleExample is OracleBase {
    TestStorage testStorage;
    event SentCallback(bytes32 queryId, string request);
    event ShowCallback(bytes32 queryId, string response, bytes32 hash);

    constructor (address _owner, address _oracleStorageAddr, address _testStorageAddr)
        OracleBase(_owner, _oracleStorageAddr)
        public
    {
        testStorage = TestStorage(_testStorageAddr);
    }

    function trigger()
        public
    {
        // all people can call this
        // maybe I need to design pause
        string memory request = 'json(https://api.kraken.com/0/public/Ticker?pair=ETHUSD)["result"]["XETHZUSD"]["c"][0]';

        bytes32 queryId = this.__querySentNode(request);
        testStorage.pushBytes32ArrayEntry('TestOracleExampleQueryIds', queryId);
        emit SentCallback(queryId, request);
    }


    function getLastestQueryId()
        view
        public
        returns (bytes32)
    {
        // all people can call this
        uint queryIdsLength = testStorage.getBytes32ArrayLength('TestOracleExampleQueryIds');
        require(queryIdsLength > 0);
        return testStorage.getBytes32ArrayEntry('TestOracleExampleQueryIds', queryIdsLength - 1);
    }

    function __callback(bytes32 _queryId, string _response, bytes32 _hash)
        onlyOwnerAndOracleCore
        public
    {
        emit ShowCallback(_queryId, _response, _hash);
    }
}
