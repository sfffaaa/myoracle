#!/usr/bin/env python3
# encoding: utf-8

import my_config
from base_object.base_contract_onchain_handler import BaseContractOnChainHandler
from chain_utils import convert_to_bytes, wait_miner, check_transaction_meet_assert

GAS_SPENT = 1000000


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
                                                               'gas': GAS_SPENT})

        wait_miner(w3, tx_hash)
        if check_transaction_meet_assert(w3, tx_hash):
            raise IOError('assert encounter..')
        print('==== query_sent_node finish ====')

    def result_sent_back(self, query_id, response, hash_val):
        print('==== result_sent_back start ====')

        self.get_contract_inst().functions.resultSentBack(convert_to_bytes(query_id),
                                                          response,
                                                          convert_to_bytes(hash_val)).call()
        print('==== result_sent_back end ====')


if __name__ == '__main__':
    pass
