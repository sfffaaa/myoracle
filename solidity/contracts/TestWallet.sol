pragma solidity 0.4.24;


contract TestWallet {
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

    function deposit()
        onlyOwner
        payable
        public
    {
        require(msg.value <= 5000 wei && msg.value >= 1000 wei);
        emit DepositAction(msg.sender, msg.value);
    }
}
