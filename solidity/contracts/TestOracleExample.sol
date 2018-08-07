pragma solidity 0.4.24;

import {OracleBase} from "./OracleBase.sol";
import {OracleRegister} from "./OracleRegister.sol";
import {TestStorage} from "./TestStorage.sol";
import {TestWalletDistributor} from "./TestWalletDistributor.sol";
import './SafeMath.sol';

contract TestOracleExample is OracleBase {
    using SafeMath for uint256;
    string TEST_WALLET_DISTRIBUTOR_ADDR_KEY = 'TestWalletDistributor';
    string TEST_STORAGE_ADDR_KEY = 'TestStorage';
    string TEST_STORAGE_QUERY_IDS_KEY = 'TestOracleExampleQueryIds';
    event SentCallback(bytes32 queryId, string request);
    event ShowCallback(bytes32 queryId, string response, bytes32 hash);
    event TriggerMyCallback(bool trigger, uint price);

    constructor (address _owner, address _oracleRegisterAddr)
        OracleBase(_owner, _oracleRegisterAddr)
        public
    {}

    function trigger()
        onlyOwner
        payable
        public
    {
        // all people can call this
        // maybe I need to design pause
        string memory request = 'json(https://api.kraken.com/0/public/Ticker?pair=ETHUSD)["result"]["XETHZUSD"]["c"][0]';

        bytes32 queryId = this.__querySentNode.value(msg.value)(0, request);

        address myTestStorageAddr = OracleRegister(myRegisterAddr).getAddress(TEST_STORAGE_ADDR_KEY);
        require(myTestStorageAddr != 0);
        TestStorage(myTestStorageAddr).pushBytes32ArrayEntry(TEST_STORAGE_QUERY_IDS_KEY, queryId);
        emit SentCallback(queryId, request);
    }


    function getLastestQueryId()
        onlyOwner
        view
        public
        returns (bytes32)
    {
        // all people can call this
        address myTestStorageAddr = OracleRegister(myRegisterAddr).getAddress(TEST_STORAGE_ADDR_KEY);
        require(myTestStorageAddr != 0);

        uint queryIdsLength = TestStorage(myTestStorageAddr).getBytes32ArrayLength(TEST_STORAGE_QUERY_IDS_KEY);
        require(queryIdsLength > 0);
        return TestStorage(myTestStorageAddr).getBytes32ArrayEntry(TEST_STORAGE_QUERY_IDS_KEY,
                                                                   queryIdsLength.sub(1));
    }

    function __callback(bytes32 _queryId, string _response, bytes32 _hash)
        onlyOwnerAndOracleCore
        public
    {
        emit ShowCallback(_queryId, _response, _hash);
        bool success = false;
        uint price = 0;
        (success, price) = convertResponseToPrice(_response);
        emit TriggerMyCallback(success, price);
        if (true == success) {
            address myTestDistributorAddr = OracleRegister(myRegisterAddr).getAddress(TEST_WALLET_DISTRIBUTOR_ADDR_KEY);
            require(myTestDistributorAddr != 0);
            TestWalletDistributor(myTestDistributorAddr).withdrawBalance(price);
        }
        //[TODO] call oracle again
    }

    // Rounddown
    function convertResponseToPrice(string _str)
        public
        pure
        returns (bool, uint)
    {
        bytes memory data = (bytes) (_str);
        uint256 price = 0;
        for (uint i = 0; i < data.length; i++) {
            // 46 => '.'
            if (data[i] == 46) {
                break;
            }
            // 48 => '0', 57 => '9'
            if (data[i] < 48 || data[i] > 57) {
                return (false, 0);
            }
            price = price.mul(10).add(uint(data[i]).sub(48));
        }

        return (true, price);
    }
}
