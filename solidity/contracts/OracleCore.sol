pragma solidity 0.4.24;


import {OracleBase} from "./OracleBase.sol";
import {OracleStorage} from "./OracleStorage.sol";

contract OracleCore {
    event ToOracleNode(bytes32 queryId, string requests);
    event ToOracleCallee(bytes32 queryId, address callee, bytes32 hash, string response);
    OracleStorage myStorage = OracleStorage(0);

    constructor (address _storage) public {
        myStorage = OracleStorage(_storage);
    }

    function querySentNode(address _callee, string _requests)
        public
        returns (bytes32 _queryId)
    {
        bytes32 myQueryId = keccak256(abi.encodePacked(now, _callee, _requests));
        myStorage.setBytes32ToAddress('OracleCoreNode', myQueryId, _callee);
        emit ToOracleNode(myQueryId, _requests);
        return myQueryId;
    }

    function resultSentBack(bytes32 _queryId, string _response, bytes32 _hash)
        external
    {
        address callee = myStorage.getBytes32ToAddress('OracleCoreNode', _queryId);
        require(callee != 0);
        emit ToOracleCallee(_queryId, callee, _hash, _response);
        OracleBase(callee).__callback(_queryId, _hash, _response);
    }
}
