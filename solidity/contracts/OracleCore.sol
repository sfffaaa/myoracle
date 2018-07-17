pragma solidity 0.4.24;


import {OracleBase} from "./OracleBase.sol";
import {OracleStorage} from "./OracleStorage.sol";

contract OracleCore {
    OracleStorage private myStorage = OracleStorage(0);
    address owner;

    event ToOracleNode(bytes32 queryId, string request);
    event ToOracleCallee(bytes32 queryId, address callee, string response, bytes32 hash);

    constructor (address _owner, address _storage) public {
        owner = _owner;
        myStorage = OracleStorage(_storage);
    }

    modifier OnlyOwner {
        require(msg.sender == owner);
        _;
    }

    function querySentNode(address _callee, string _requests)
        public
        returns (bytes32)
    {
        // all user can call this
        bytes32 myQueryId = keccak256(abi.encodePacked(now, _callee, _requests));
        myStorage.setBytes32ToAddress('OracleCoreNode', myQueryId, _callee);
        emit ToOracleNode(myQueryId, _requests);
        return myQueryId;
    }

    function resultSentBack(bytes32 _queryId, string _response, bytes32 _hash)
        OnlyOwner
        external
    {
        // only some register node and owner can call this
        address callee = myStorage.getBytes32ToAddress('OracleCoreNode', _queryId);
        require(callee != 0);
        emit ToOracleCallee(_queryId, callee, _response, _hash);
        OracleBase(callee).__callback(_queryId, _response, _hash);
    }
}
