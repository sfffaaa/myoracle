pragma solidity 0.4.24;

import {OracleConstant} from "./OracleConstant.sol";
import {OracleStorage} from "./OracleStorage.sol";
import {OracleRegister} from "./OracleRegister.sol";
import './SafeMath.sol';


contract OracleFeeWallet is OracleConstant {
    using SafeMath for uint256;
    address oracleRegisterAddr;
    address owner;

    event DepositAction(address  sender, uint value, uint accumulateValue);
    event UpdateUsedAction(address  helperAddr, address  balanceAddr,
                           uint value, uint accumulateValue);
    event UpdatePaybackAction(address  helperAddr, address  balanceAddr,
                              uint value, uint accumulateValue);
    event PaybackAction(address paybackAddr, uint paybackValue);


    constructor (address _owner, address _oracleRegisterAddr) public {
        owner = _owner;
        oracleRegisterAddr = _oracleRegisterAddr;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    function registerClientAddr(address _addr)
        onlyOwner
        external
    {
        require(_addr != 0);
        address myStorageAddr = OracleRegister(oracleRegisterAddr).getAddress(ORACLE_STORAGE_ADDR_KEY);
        require(myStorageAddr != 0);

        uint idxP1 = OracleStorage(myStorageAddr).getAddressToUint(
            "OracleFeeWalletClientRegisterAddrToIdxP1",
            _addr
        );

        if (0 == idxP1) {
            OracleStorage(myStorageAddr).pushBytes32AddressArrayEntry(
                "OracleFeeWalletClientRegisterAddrList",
                _addr
            );
            uint length = OracleStorage(myStorageAddr).getBytes32AddressArrayLength(
                "OracleFeeWalletClientRegisterAddrList"
            );
            OracleStorage(myStorageAddr).setAddressToUint(
                "OracleFeeWalletClientRegisterAddrToIdxP1",
                _addr,
                length
            );
        }
    }

    function deregisterClientAddr(address _addr)
        onlyOwner
        external
    {
        require(_addr != 0);
        address myStorageAddr = OracleRegister(oracleRegisterAddr).getAddress(ORACLE_STORAGE_ADDR_KEY);
        require(myStorageAddr != 0);

        uint idxP1 = OracleStorage(myStorageAddr).getAddressToUint(
            "OracleFeeWalletClientRegisterAddrToIdxP1",
            _addr
        );

        if (idxP1 == 0) {
            return;
        }

        uint idx = idxP1 - 1;
        uint length = OracleStorage(myStorageAddr).getBytes32AddressArrayLength(
            "OracleFeeWalletClientRegisterAddrList"
        );
        uint lastIdx = length - 1;
        address lastAddr = OracleStorage(myStorageAddr).getBytes32AddressArrayEntry(
            "OracleFeeWalletClientRegisterAddrList",
            lastIdx
        );
        OracleStorage(myStorageAddr).setBytes32AddressArrayEntry(
            "OracleFeeWalletClientRegisterAddrList",
            idx,
            lastAddr
        );
        OracleStorage(myStorageAddr).setAddressToUint(
            "OracleFeeWalletClientRegisterAddrToIdxP1",
            lastAddr,
            idx + 1
        );

        OracleStorage(myStorageAddr).delBytes32AddressArrayEntry(
            "OracleFeeWalletClientRegisterAddrList",
            lastIdx
        );

        OracleStorage(myStorageAddr).setAddressToUint(
            "OracleFeeWalletClientRegisterAddrToIdxP1",
            _addr,
            0
        );
    }

    modifier checkOwnerAndRegister() {
        bool checked = false;
        if (msg.sender == owner) {
            checked = true;
        } else {
            address myStorageAddr = OracleRegister(oracleRegisterAddr).getAddress(ORACLE_STORAGE_ADDR_KEY);
            require(myStorageAddr != 0);
            uint length = OracleStorage(myStorageAddr).getBytes32AddressArrayLength(
                "OracleFeeWalletClientRegisterAddrList"
            );
            for (uint i = 0; i < length; i++) {
                address checkAddr = OracleStorage(myStorageAddr).getBytes32AddressArrayEntry(
                    "OracleFeeWalletClientRegisterAddrList",
                    i
                );
                if (checkAddr == msg.sender) {
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
        external
    {
        address myStorageAddr = OracleRegister(oracleRegisterAddr).getAddress(ORACLE_STORAGE_ADDR_KEY);
        require(myStorageAddr != 0);

        uint length = OracleStorage(myStorageAddr).getBytes32AddressArrayLength(
            'OracleFeeWalletPaybackAddrList'
        );
        for (uint idxP1 = length; idxP1 > 0; idxP1--) {
            uint realIdx = idxP1 - 1;
            address paybackAddr = OracleStorage(myStorageAddr).getBytes32AddressArrayEntry(
                'OracleFeeWalletPaybackAddrList',
                realIdx
            );
            uint paybackValue = OracleStorage(myStorageAddr).getAddressToUint(
                "OracleFeeWalletPaybackValueMap",
                paybackAddr
            );
            if (paybackValue != 0) {
                require(address(this).balance >= paybackValue);
                paybackAddr.transfer(paybackValue);
                emit PaybackAction(paybackAddr, paybackValue);
                OracleStorage(myStorageAddr).setAddressToUint(
                    "OracleFeeWalletPaybackValueMap",
                    paybackAddr,
                    0
                );
            }
            OracleStorage(myStorageAddr).setAddressToUint(
                "OracleFeeWalletPaybackAddrToIdxP1",
                paybackAddr,
                0
            );
            OracleStorage(myStorageAddr).delBytes32AddressArrayEntry(
                'OracleFeeWalletPaybackAddrList',
                realIdx
            );
        }
    }

    // [TODO] Not implement right now
    function returnAllMoney()
        onlyOwner
        external
        view
    {
        require(1 == 0);
    }

    // [TODO] Should be internal function (?
    function updateUsedBalance(address _addr, uint _value)
        checkOwnerAndRegister
        external
    {
        require(_addr != 0);

        address myStorageAddr = OracleRegister(oracleRegisterAddr).getAddress(ORACLE_STORAGE_ADDR_KEY);
        require(myStorageAddr != 0);

        uint remainValue = OracleStorage(myStorageAddr).getAddressToUint(
            "OracleFeeWalletAddressValueMap",
            _addr
        );
        require(remainValue >= _value);
        remainValue = remainValue.sub(_value);
        OracleStorage(myStorageAddr).setAddressToUint(
            "OracleFeeWalletAddressValueMap",
            _addr,
            remainValue
        );

        uint paybackValue = OracleStorage(myStorageAddr).getAddressToUint(
            "OracleFeeWalletPaybackValueMap",
            msg.sender
        );
        paybackValue = paybackValue.add(_value);
        OracleStorage(myStorageAddr).setAddressToUint(
            "OracleFeeWalletPaybackValueMap",
            msg.sender,
            paybackValue
        );
        
        uint idxP1 = OracleStorage(myStorageAddr).getAddressToUint(
            "OracleFeeWalletPaybackAddrToIdxP1",
            msg.sender
        );
        if (0 == idxP1) {
            OracleStorage(myStorageAddr).pushBytes32AddressArrayEntry(
                'OracleFeeWalletPaybackAddrList',
                msg.sender
            );
            uint length = OracleStorage(myStorageAddr).getBytes32AddressArrayLength(
                'OracleFeeWalletPaybackAddrList'
            );
            OracleStorage(myStorageAddr).setAddressToUint(
                "OracleFeeWalletPaybackAddrToIdxP1",
                msg.sender,
                length
            );       
        }

        emit UpdatePaybackAction(msg.sender, _addr, _value, paybackValue);
        emit UpdateUsedAction(msg.sender, _addr, _value, remainValue);
    }

    // [TODO] Only register node addrress can do this (or owner)
    function getBalance(address _addr)
        external
        view
        returns (uint)
    {
        require(_addr != 0);
        address myStorageAddr = OracleRegister(oracleRegisterAddr).getAddress(ORACLE_STORAGE_ADDR_KEY);
        require(myStorageAddr != 0);

        return OracleStorage(myStorageAddr).getAddressToUint(
            "OracleFeeWalletAddressValueMap",
            _addr
        );
    }

    function deposit()
        payable
        public
    {
        address sender = msg.sender;
        address myStorageAddr = OracleRegister(oracleRegisterAddr).getAddress(ORACLE_STORAGE_ADDR_KEY);
        require(myStorageAddr != 0);

        uint value = OracleStorage(myStorageAddr).getAddressToUint(
            "OracleFeeWalletAddressValueMap",
            sender
        );
        value = value.add(msg.value);
        OracleStorage(myStorageAddr).setAddressToUint(
            "OracleFeeWalletAddressValueMap",
            sender,
            value
        );
        emit DepositAction(sender, msg.value, value);
    }
}
