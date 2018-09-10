pragma solidity 0.4.24;

import {OracleRegister} from "./OracleRegister.sol";
import {OracleCore} from "./OracleCore.sol";
import {OracleConstant} from "./OracleConstant.sol";
import {OracleFeeWallet} from "./OracleFeeWallet.sol";

// OracleBase and its childs need deploy after oracleCore and OracleStorage.
contract OracleBase is OracleConstant {
   
    address myRegisterAddr;
    address owner;

    constructor (address _owner, address _oracleRegisterAddr)
        public
    {
        require(_owner != 0);
        require(_oracleRegisterAddr != 0);
        owner = _owner;
        myRegisterAddr = _oracleRegisterAddr;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    modifier onlyOwnerAndMyself {
        require(msg.sender == address(this) || msg.sender == owner);
        _;
    }

    modifier onlyOwnerAndOracleCore {
        address oracleCoreAddress = OracleRegister(myRegisterAddr).getAddress(ORACLE_CORE_ADDR_KEY);
        require(oracleCoreAddress != 0);
        require(msg.sender == owner || msg.sender == oracleCoreAddress);
        _;
    }

    function __querySentNode(uint timeout, string _requests)
        onlyOwnerAndMyself
        public
        returns (bytes32)
    {
        // only self and owner can call this
        address oracleCoreAddress = OracleRegister(myRegisterAddr).getAddress(ORACLE_CORE_ADDR_KEY);
        require(oracleCoreAddress != 0);

        return OracleCore(oracleCoreAddress).querySentNode(timeout, address(this), _requests);
    }

    function __callback(bytes32 _queryId, string _response, bytes32 _hash) external;

    function deposit()
        onlyOwner
        payable
        external
    {
        address oracleFeeWalletAddr = OracleRegister(myRegisterAddr).getAddress(ORACLE_FEE_WALLET_ADDR_KEY);
        require(oracleFeeWalletAddr != 0);
        OracleFeeWallet(oracleFeeWalletAddr).deposit.value(msg.value)();
    }
}
