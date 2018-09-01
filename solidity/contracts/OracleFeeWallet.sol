pragma solidity 0.4.24;

import {OracleConstant} from "./OracleConstant.sol";
import './SafeMath.sol';


contract OracleFeeWallet is OracleConstant {
    using SafeMath for uint256;

    address owner;
    mapping(address => uint) addressValueMap;
    mapping(address => uint) paybackValueMap;

    event DepositAction(address sender, uint value, uint accumulateValue);
    event WithdrawAction(address sender, uint value);


    constructor (address _owner) public {
        owner = _owner;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    // [TODO] Not implement
    function payback()
        onlyOwner
        public
        view
    {
        // [TODO] Force stop because I'm not finish yet
        assert(0 == 1);
    }

    // [TODO] Not implement
    function withdraw(address _outAddr)
        onlyOwner
        payable
        public
    {
        assert(0 == 1);
        _outAddr.transfer(address(this).balance);
        emit WithdrawAction(_outAddr, address(this).balance);
    }

    function getBalance(address _addr)
        public
        view
        returns (uint)
    {
        return addressValueMap[_addr];
    }

    function deposit()
        payable
        public
    {
        address sender = msg.sender;
        addressValueMap[sender] = addressValueMap[sender].add(msg.value);
        emit DepositAction(sender, msg.value, addressValueMap[sender]);
    }
}
