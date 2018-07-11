#!/usr/bin/env python3
# encoding: utf-8

import my_config
from contract_handler import ContractHandler
from chain_utils import convert_to_bytes, wait_miner, check_transaction_meet_assert

GAS_SPENT = 1000000


class OracleCoreOnChainHandler():

    def __init__(self, config_path=my_config.CONFIG_PATH):
        self._contract_handler = ContractHandler('OracleCore', config_path)
        self._w3 = self._contract_handler.get_w3()
        self._contract_inst = self._contract_handler.get_contract()

    def get_all_events(self):
        return self._contract_handler.get_all_events()

    def query_sent_node(self, address, requests):
        print('==== query_sent_node start ====')
        tx_hash = self._contract_inst.functions.querySentNode(address, requests) \
                                               .transact({'from': self._w3.eth.accounts[0],
                                                          'gas': GAS_SPENT})

        wait_miner(self._w3, tx_hash)
        if check_transaction_meet_assert(self._w3, tx_hash):
            raise IOError('assert encounter..')
        print('==== query_sent_node finish ====')

    def result_sent_back(self, query_id, response, hash_val):
        print('==== result_sent_back start ====')

        self._contract_inst.functions.resultSentBack(convert_to_bytes(query_id),
                                                     response,
                                                     convert_to_bytes(hash_val)).call()
        print('==== result_sent_back end ====')


if __name__ == '__main__':
    pass
