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

    event DepositAction(address  sender, uint value, uint accumulateValue);
    event UpdateUsedAction(address  helperAddr, address  balanceAddr,
                           uint value, uint accumulateValue);
    event UpdatePaybackAction(address  helperAddr, address  balanceAddr,
                              uint value, uint accumulateValue);
    event PaybackAction(address paybackAddr, uint paybackValue);


    constructor (address _owner) public {
        owner = _owner;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    function payback()
        onlyOwner
        public
    {
        for (uint idxP1 = paybackAddrList.length; idxP1 > 0; idxP1--) {
            uint realIdx = idxP1 - 1;
            address paybackAddr = paybackAddrList[realIdx];
            uint paybackValue = paybackValueMap[paybackAddr];
            if (paybackValue != 0) {
                paybackAddr.transfer(paybackValue);
                emit PaybackAction(paybackAddr, paybackValue);
            }
            paybackValueMap[paybackAddr] = 0;
            paybackAddrToIdxP1[paybackAddr] = 0;
            delete paybackAddrList[realIdx];
        }
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

        emit UpdatePaybackAction(msg.sender, _addr, _value, paybackValueMap[msg.sender]);
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
