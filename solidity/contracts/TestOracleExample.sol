pragma solidity 0.4.24;

import {OracleBase} from "./OracleBase.sol";
import {OracleRegister} from "./OracleRegister.sol";
import {TestStorage} from "./TestStorage.sol";

contract TestOracleExample is OracleBase {
    event SentCallback(bytes32 queryId, string request);
    event ShowCallback(bytes32 queryId, string response, bytes32 hash);

    constructor (address _owner, address _oracleRegisterAddr)
        OracleBase(_owner, _oracleRegisterAddr)
        public
    {}

    function trigger()
        public
    {
        // all people can call this
        // maybe I need to design pause
        string memory request = 'json(https://api.kraken.com/0/public/Ticker?pair=ETHUSD)["result"]["XETHZUSD"]["c"][0]';

        bytes32 queryId = this.__querySentNode(request);

        address myTestStorageAddr = OracleRegister(myRegisterAddr).getAddress('TestStorage');
        require(myTestStorageAddr != 0);
        TestStorage(myTestStorageAddr).pushBytes32ArrayEntry('TestOracleExampleQueryIds', queryId);
        emit SentCallback(queryId, request);
    }


    function getLastestQueryId()
        view
        public
        returns (bytes32)
    {
        // all people can call this
        address myTestStorageAddr = OracleRegister(myRegisterAddr).getAddress('TestStorage');
        require(myTestStorageAddr != 0);

        uint queryIdsLength = TestStorage(myTestStorageAddr).getBytes32ArrayLength('TestOracleExampleQueryIds');
        require(queryIdsLength > 0);
        return TestStorage(myTestStorageAddr).getBytes32ArrayEntry('TestOracleExampleQueryIds',
                                                                   queryIdsLength - 1);
    }

    function __callback(bytes32 _queryId, string _response, bytes32 _hash)
        onlyOwnerAndOracleCore
        public
    {
        emit ShowCallback(_queryId, _response, _hash);
    }
}
