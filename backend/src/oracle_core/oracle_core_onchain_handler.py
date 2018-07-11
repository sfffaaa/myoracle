#!/usr/bin/env python3
# encoding: utf-8

from utils import my_config
from base_object.base_contract_onchain_handler import BaseContractOnChainHandler
from utils.chain_utils import convert_to_bytes, wait_miner, check_transaction_meet_assert


class OracleCoreOnChainHandler(BaseContractOnChainHandler):

    def __init__(self, config_path=my_config.CONFIG_PATH):
        super().__init__(config_path)

    # --- implement base class ---
    def get_contract_handler_name(self):
        return 'OracleCore'

    # --- connect to contract function ---
    def query_sent_node(self, address, requests):
        w3 = self.get_w3_inst()
        print('==== query_sent_node start ====')
        tx_hash = self.get_contract_inst().functions.querySentNode(address, requests) \
                                                    .transact({'from': w3.eth.accounts[0],
                                                               'gas': my_config.GAS_SPENT})

        wait_miner(w3, tx_hash)
        if check_transaction_meet_assert(w3, tx_hash):
            raise IOError('assert encounter..')
        print('==== query_sent_node finish ====')

    def result_sent_back(self, query_id, response, hash_val):
        w3 = self.get_w3_inst()
        print('==== result_sent_back start ====')

        tx_hash = self.get_contract_inst().functions.resultSentBack(convert_to_bytes(query_id),
                                                                    response,
                                                                    convert_to_bytes(hash_val)) \
                                                    .transact({'from': w3.eth.accounts[0],
                                                               'gas': my_config.GAS_SPENT})
        wait_miner(w3, tx_hash)
        if check_transaction_meet_assert(w3, tx_hash):
            raise IOError('assert encounter..')
        print('==== result_sent_back end ====')


if __name__ == '__main__':
    pass
