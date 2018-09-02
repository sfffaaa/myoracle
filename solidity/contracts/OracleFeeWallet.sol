pragma solidity 0.4.24;

import {OracleConstant} from "./OracleConstant.sol";
import './SafeMath.sol';


contract OracleFeeWallet is OracleConstant {
    using SafeMath for uint256;

    address owner;
    mapping(address => uint) private addressValueMap;
    mapping(address => uint) private paybackValueMap;

    address[] private paybackAddrList;
    mapping(address => uint) private paybackAddrToIdxP1;

    event DepositAction(address indexed sender, uint value, uint accumulateValue);
    event UpdateUsedAction(address indexed helperAddr, address indexed balanceAddr,
                           uint value, uint accumulateValue);
    event UpdatePaybackAction(address indexed helperAddr, address indexed balanceAddr,
                              uint value, uint accumulateValue);
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

    // [TODO] Only register node address can do this (or owner)
    // [TODO] Should be internal function (?
    function updateUsedBalance(address _addr, uint _value)
        public
    {
        uint remainValue = addressValueMap[_addr];
        require(remainValue >= _value);
        addressValueMap[_addr] = remainValue.sub(_value);

        paybackValueMap[msg.sender] = paybackValueMap[msg.sender].add(_value);
        
        uint idxP1 = paybackAddrToIdxP1[msg.sender];
        if (0 == idxP1) {
            paybackAddrList.push(msg.sender);
            paybackAddrToIdxP1[msg.sender] = paybackAddrList.length;
        }

        emit UpdatePaybackAction(msg.sender, _addr, _value, paybackValueMap[_addr]);
        emit UpdateUsedAction(msg.sender, _addr, _value, addressValueMap[_addr]);
    }

    // [TODO] Only register node addrress can do this (or owner)
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
