pragma solidity 0.4.24;


import {OracleBase} from "./OracleBase.sol";

contract OracleCore {
    //[TODO] Should extract below storage to specific smart contract
    mapping (bytes32 => address) public queryId2Address;
    event ToOracleNode(bytes32 queryId, string requests);
    event ToOracleCallee(bytes32 queryId, address callee, bytes32 hash, string response);

    function querySentNode(address _callee, string _requests)
        public
        returns (bytes32 _queryId)
    {
        bytes32 myQueryId = keccak256(abi.encodePacked(now, _callee, _requests));
        queryId2Address[myQueryId] = _callee;
        emit ToOracleNode(myQueryId, _requests);
        return myQueryId;
    }

    function resultSentBack(bytes32 _queryId, string _response, bytes32 _hash)
        external
    {
        require(queryId2Address[_queryId] != 0);
        address callee = queryId2Address[_queryId];
        emit ToOracleCallee(_queryId, callee, _hash, _response);
        OracleBase(callee).__callback(_queryId, _hash, _response);
    }
}
