pragma solidity 0.4.24;

import './SafeMath.sol';


contract TestWalletDistributor {
    using SafeMath for uint256;

    address myAddress;
    uint threshold;
    event DepositBalance(address myAddress, uint threshold, uint nowValue, uint accuValue);
    event WithdrawBalance(address myAddress, uint threshold, uint value, uint price, bool transfered);
    
    constructor(address _myAddress)
        public
    {
        myAddress = _myAddress;
    }

    function depositBalance(uint _threshold)
        payable
        public
    {
        require(0 != _threshold);
        threshold = _threshold;

        require(myAddress == msg.sender);
        emit DepositBalance(myAddress, threshold, msg.value, address(this).balance);
    }

    function withdrawBalance(uint _price)
        public
    {
        uint myBalance = address(this).balance;
        if (_price < threshold) {
            emit WithdrawBalance(myAddress, threshold, myBalance, _price, false);
            return;
        }
        myAddress.transfer(myBalance);
        emit WithdrawBalance(myAddress, threshold, myBalance, _price, true);
    }
}
