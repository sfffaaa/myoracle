pragma solidity 0.4.24;

contract OracleConstant {
    string constant ORACLE_CORE_ADDR_KEY = 'OracleCore';
    string constant ORACLE_STORAGE_ADDR_KEY = 'OracleStorage';
    string constant ORACLE_NODE_ADDR_KEY = 'OracleCoreNode';

    string constant ORACLE_ADDR_KEY = 'OracleAddress';

    uint constant MIN_PAYMENT_AMOUNT = 1000 wei;
    uint constant MAX_PAYMENT_AMOUNT = 5000 wei;
}
