pragma solidity 0.4.24;

import {OracleConstant} from "./OracleConstant.sol";


contract OracleWallet is OracleConstant {
    address owner;
    event DepositAction(address sender, uint value);
    event WithdrawAction(address sender, uint value);


    constructor (address _owner) public {
        owner = _owner;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

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
        require(msg.value <= MAX_PAYMENT_AMOUNT && msg.value >= MIN_PAYMENT_AMOUNT);
        emit DepositAction(_sender, msg.value);
    }
}
