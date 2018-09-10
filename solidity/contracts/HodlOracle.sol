pragma solidity 0.4.24;

import {OracleBase} from "./OracleBase.sol";
import {HodlRegister} from "./HodlRegister.sol";
import {HodlStorage} from "./HodlStorage.sol";
import {HodlSaver} from "./HodlSaver.sol";
import './SafeMath.sol';

contract HodlOracle is OracleBase {
    using SafeMath for uint256;
    string HODL_SAVER_ADDR_KEY = 'HodlSaver';
    string HODL_STORAGE_ADDR_KEY = 'HodlStorage';
    string HODL_ORACLE_QUERY_IDS_KEY = 'HodlOracleQueryIds';
    event SentCallback(bytes32 queryId, string request);
    event ShowCallback(bytes32 queryId, string response, bytes32 hash);
    event TriggerMyCallback(bool trigger, uint price);
    address hodlRegisterAddr;

    constructor (address _owner, address _oracleRegisterAddr, address _hodlRegisterAddr)
        OracleBase(_owner, _oracleRegisterAddr)
        public
    {
        hodlRegisterAddr = _hodlRegisterAddr;
    }

    function trigger()
        onlyOwner
        public
    {
        // all people can call this
        // maybe I need to design pause
        string memory request = 'json(https://api.kraken.com/0/public/Ticker?pair=ETHUSD)["result"]["XETHZUSD"]["c"][0]';

        bytes32 queryId = this.__querySentNode(0, request);

        address myHodlStorageAddr = HodlRegister(hodlRegisterAddr).getAddress(HODL_STORAGE_ADDR_KEY);
        require(myHodlStorageAddr != 0);
        HodlStorage(myHodlStorageAddr).pushBytes32ArrayEntry(HODL_ORACLE_QUERY_IDS_KEY, queryId);
        emit SentCallback(queryId, request);
    }


    function getLastestQueryId()
        onlyOwner
        view
        external
        returns (bytes32)
    {
        // all people can call this
        address myHodlStorageAddr = HodlRegister(hodlRegisterAddr).getAddress(HODL_STORAGE_ADDR_KEY);
        require(myHodlStorageAddr != 0);

        uint queryIdsLength = HodlStorage(myHodlStorageAddr).getBytes32ArrayLength(HODL_ORACLE_QUERY_IDS_KEY);
        require(queryIdsLength > 0);
        return HodlStorage(myHodlStorageAddr).getBytes32ArrayEntry(HODL_ORACLE_QUERY_IDS_KEY,
                                                                   queryIdsLength.sub(1));
    }

    function __callback(bytes32 _queryId, string _response, bytes32 _hash)
        onlyOwnerAndOracleCore
        external
    {
        emit ShowCallback(_queryId, _response, _hash);
        bool success = false;
        uint price = 0;
        (success, price) = convertResponseToPrice(_response);
        emit TriggerMyCallback(success, price);
        if (true == success) {
            address myHodlSaverAddr = HodlRegister(hodlRegisterAddr).getAddress(HODL_SAVER_ADDR_KEY);
            require(myHodlSaverAddr != 0);
            HodlSaver(myHodlSaverAddr).withdrawBalance(price);
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
