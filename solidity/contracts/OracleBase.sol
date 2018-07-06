pragma solidity 0.4.24;

contract OracleBase {
    function __callback(bytes32 _queryId, bytes32 _hash, string _response) public;
}
