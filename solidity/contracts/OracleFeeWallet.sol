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

    address[] private clientRegisterAddrList;
    mapping(address => uint) private clientRegisterAddrToIdxP1;

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

    function registerClientAddr(address _addr)
        onlyOwner
        public
    {
        require(_addr != 0);
        if (0 == clientRegisterAddrToIdxP1[_addr]) {
            clientRegisterAddrList.push(_addr);
            clientRegisterAddrToIdxP1[_addr] = clientRegisterAddrList.length;
        }
    }

    function deregisterClientAddr(address _addr)
        onlyOwner
        public
    {
        require(_addr != 0);

        uint idxP1 = clientRegisterAddrToIdxP1[_addr];
        if (idxP1 == 0) {
            return;
        }

        uint idx = idxP1 - 1;
        uint lastIdx = clientRegisterAddrList.length - 1;
        address lastAddr = clientRegisterAddrList[lastIdx];
        clientRegisterAddrList[idx] = clientRegisterAddrList[lastIdx];
        clientRegisterAddrToIdxP1[lastAddr] = idx + 1;

        delete clientRegisterAddrList[lastIdx];
        clientRegisterAddrToIdxP1[_addr] = 0;
    }

    modifier checkOwnerAndRegister() {
        bool checked = false;
        if (msg.sender == owner) {
            checked = true;
        } else {
            for (uint i = 0; i < clientRegisterAddrList.length; i++) {
                if (clientRegisterAddrList[i] == msg.sender) {
                    checked = true;
                    break;
                }
            }
        }
        require(checked == true);

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

    // [TODO] Not implement right now
    function returnAllMoney()
        onlyOwner
        public
        view
    {
        require(1 == 0);
    }

    // [TODO] Should be internal function (?
    function updateUsedBalance(address _addr, uint _value)
        checkOwnerAndRegister
        public
    {
        require(_addr != 0);

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
        require(_addr != 0);
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
