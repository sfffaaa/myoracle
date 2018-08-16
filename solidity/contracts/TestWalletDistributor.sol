pragma solidity 0.4.24;

import './SafeMath.sol';


contract TestWalletDistributor {
    using SafeMath for uint256;

    struct Entry {
        uint indexA1;
        uint threshold;
        uint value;
    }
    address[] myAddresses;
    mapping(address => Entry) myAddressMapping;

    event DepositBalance(address myAddress, uint threshold, uint nowValue, uint accuValue);
    event WithdrawBalance(address myAddress, uint threshold, uint value, uint price, bool transfered);
    
    constructor()
        public
    {}

    function depositBalance(uint _threshold)
        payable
        public
    {
        address sender = msg.sender;
        require(0 != _threshold);
        Entry memory entry = myAddressMapping[sender];
        if (entry.indexA1 == 0) {
            entry.indexA1 = myAddresses.length + 1;
            entry.threshold = _threshold;
            entry.value = msg.value;
            myAddresses.push(sender);
        } else {
            entry.threshold = _threshold;
            entry.value = entry.value.add(msg.value);
        }
        myAddressMapping[sender] = entry;

        emit DepositBalance(sender, _threshold, msg.value, entry.value);
    }

    function withdrawBalance(uint _price)
        public
    {
        for (uint i = 0; i < myAddresses.length; i++) {
            address testAddress = myAddresses[i];
            Entry memory entry = myAddressMapping[testAddress];
            if (0 == entry.value || _price < entry.threshold) {
                emit WithdrawBalance(testAddress, entry.threshold, entry.value, _price, false);
                continue;
            }

            testAddress.transfer(entry.value);
            emit WithdrawBalance(testAddress, entry.threshold, entry.value, _price, true);
            // Remove that data
            entry.value = 0;
            myAddressMapping[testAddress] = entry;
        }
    }
}
