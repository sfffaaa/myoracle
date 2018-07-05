pragma solidity 0.4.24;

contract OracleCore {
    mapping (bytes32 => address) queryId2Address;
    event ToOracleNode(bytes32 queryId, string requests);

    function QuerySentNode(address _callee, string _requests)
        public
        returns (bytes32 _queryId)
    {
        bytes32 myQueryId = keccak256(now, _callee, _requests);
        ToOracleNode(myQueryId, _requests);
        queryId2Address[myQueryId] = _callee;
        return myQueryId;
    }

    function ResultSentBack(bytes32 _queryId, string _response)
        external {
        require(queryId2Address[_queryId] != 0);
        address callee = queryId2Address[_queryId];

        //__callack(bytes32 _queryId, string _response, bytes32 _hash);
        require(callee.call(bytes4(keccak256("__callback(bytes32,string,bytes32)")), _response));
    }
}
