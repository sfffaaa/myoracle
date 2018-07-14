pragma solidity 0.4.24;

import {OracleBase} from "./OracleBase.sol";
import {OracleStorage} from "./OracleStorage.sol";

contract TestOracleExample is OracleBase {
    event SentCallback(bytes32 queryId, string request);
    event ShowCallback(bytes32 queryId, string response, bytes32 hash);

    constructor (address _owner, address _oracleStorage) OracleBase(_owner, _oracleStorage)
        public
    {}

    function trigger()
        public
    {
        // all people can call this
        // maybe I need to design pause
        string memory request = 'json(https://api.kraken.com/0/public/Ticker?pair=ETHUSD)["result"]["XETHZUSD"]["c"][0]';
        //[TODO] Need to change this or maybe change permission setting...
        this.querySentNode(request);
    }

    //[TODO] This function can be intergreted into trigger...
    function querySentNode(string _data)
        onlyOwnerAndMyself
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
        // all people can call this
        uint queryIdsLength = OracleStorage(myStorageAddr).getBytes32ArrayLength('TestOracleExampleQueryIds');
        require(queryIdsLength > 0);
        return OracleStorage(myStorageAddr).getBytes32ArrayEntry('TestOracleExampleQueryIds', queryIdsLength - 1);
    }

    function __callback(bytes32 _queryId, string _response, bytes32 _hash)
        onlyOwnerAndOracleCore
        public
    {
        emit ShowCallback(_queryId, _response, _hash);
    }
}
