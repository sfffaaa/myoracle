pragma solidity 0.4.24;

import {OracleConstant} from "./OracleConstant.sol";
import {OracleRegister} from "./OracleRegister.sol";
import {OracleFeeWallet} from "./OracleFeeWallet.sol";


contract OracleWallet is OracleConstant {
    address owner;
    address oracleRegisterAddr;
    event DepositAction(address sender, uint value);
    event WithdrawAction(address sender, uint value);


    constructor (address _owner, address _oracleRegisterAddr)
        public
    {
        owner = _owner;
        oracleRegisterAddr = _oracleRegisterAddr;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    modifier onlyOwnerAndOracleCore {
        require(msg.sender == owner ||
                msg.sender == OracleRegister(oracleRegisterAddr).getAddress(ORACLE_CORE_ADDR_KEY));
        _;
    }

    function () payable public {}

    function withdraw(address _outAddr)
        onlyOwner
        payable
        public
    {
        _outAddr.transfer(address(this).balance);
        emit WithdrawAction(_outAddr, address(this).balance);
    }

    function deposit(address _sender)
        payable
        public
    {
        emit DepositAction(_sender, msg.value);
    }

    function updateUsedBalance(address _addr, uint _value)
        onlyOwnerAndOracleCore
        public
    {
        address myFeeWalletAddr = OracleRegister(oracleRegisterAddr).getAddress(ORACLE_FEE_WALLET_ADDR_KEY);
        OracleFeeWallet(myFeeWalletAddr).updateUsedBalance(_addr, _value);
    }
}
