pragma solidity 0.4.24;


import {OracleBase} from "./OracleBase.sol";
import {OracleStorage} from "./OracleStorage.sol";
import {OracleRegister} from "./OracleRegister.sol";
import {OracleConstant} from "./OracleConstant.sol";
import {OracleWallet} from "./OracleWallet.sol";
import {OracleFeeWallet} from "./OracleFeeWallet.sol";


contract OracleCore is OracleConstant {
    address owner;
    address oracleRegisterAddr;

    event ToOracleNode(uint timeout, bytes32 queryId, string request);
    event ToOracleCallee(bytes32 queryId, address callee, string response, bytes32 hash);

    constructor (address _owner, address _oracleRegisterAddr) public {
        owner = _owner;
        oracleRegisterAddr = _oracleRegisterAddr;
    }

    modifier OnlyOwner {
        require(msg.sender == owner);
        _;
    }

    //[TODO] Check the callee...
    function querySentNode(uint timeout, address _callee, string _requests)
        payable
        public
        returns (bytes32)
    {

        require(oracleRegisterAddr != 0);
        address myStorageAddr = OracleRegister(oracleRegisterAddr).getAddress(ORACLE_STORAGE_ADDR_KEY);
        require(myStorageAddr != 0);

        // all user can call this
        bytes32 myQueryId = keccak256(abi.encodePacked(now, _callee, _requests));
        OracleStorage(myStorageAddr).setBytes32ToAddress(ORACLE_NODE_ADDR_KEY, myQueryId, _callee);
        emit ToOracleNode(timeout, myQueryId, _requests);

        address myWalletAddr = OracleRegister(oracleRegisterAddr).getAddress(ORACLE_WALLET_ADDR_KEY);
        require(myWalletAddr != 0);
        OracleWallet(myWalletAddr).updateUsedBalance(_callee, 10000);

        return myQueryId;
    }

    function resultSentBack(bytes32 _queryId, string _response, bytes32 _hash)
        OnlyOwner
        external
    {
        //uint leftGas = gasleft();

        require(oracleRegisterAddr != 0);
        address myStorageAddr = OracleRegister(oracleRegisterAddr).getAddress(ORACLE_STORAGE_ADDR_KEY);
        require(myStorageAddr != 0);

        // only some register node and owner can call this
        address callee = OracleStorage(myStorageAddr).getBytes32ToAddress(ORACLE_NODE_ADDR_KEY, _queryId);
        require(callee != 0);

        address myWalletAddr = OracleRegister(oracleRegisterAddr).getAddress(ORACLE_WALLET_ADDR_KEY);
        require(myWalletAddr != 0);
        OracleWallet(myWalletAddr).updateUsedBalance(callee, 10000);

        emit ToOracleCallee(_queryId, callee, _response, _hash);
        OracleBase(callee).__callback(_queryId, _response, _hash);

    }
}
