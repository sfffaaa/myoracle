#!/usr/bin/env python3
# encoding: utf-8

from utils import my_config
from base_object.base_contract_onchain_handler import BaseContractOnChainHandler
from utils.chain_utils import convert_to_bytes


class OracleCoreOnChainHandler(BaseContractOnChainHandler):

    def __init__(self, config_path=my_config.CONFIG_PATH):
        super().__init__(config_path)

    # --- implement base class ---
    def get_contract_handler_name(self):
        return 'OracleCore'

    # --- connect to contract function ---
    def set_oracle_core_addr(self, **kargs):
        transaction_data = self.compose_transaction_dict(kargs)
        print('==== set_oracle_core_addr start ====')
        tx_hash = self.get_contract_inst().functions.setOracleCoreAddr() \
                                                    .transact(transaction_data)

        self.wait_miner_finish(tx_hash)
        print('==== set_oracle_core_addr finish ====')

    def query_sent_node(self, address, requests, **kargs):
        transaction_data = self.compose_transaction_dict(kargs)
        print('==== query_sent_node start ====')
        tx_hash = self.get_contract_inst().functions.querySentNode(address, requests) \
                                                    .transact(transaction_data)

        self.wait_miner_finish(tx_hash)
        print('==== query_sent_node finish ====')

    def result_sent_back(self, query_id, response, hash_val, **kargs):
        transaction_data = self.compose_transaction_dict(kargs)
        print('==== result_sent_back start ====')

        tx_hash = self.get_contract_inst().functions.resultSentBack(convert_to_bytes(query_id),
                                                                    response,
                                                                    convert_to_bytes(hash_val)) \
                                                    .transact(transaction_data)
        self.wait_miner_finish(tx_hash)
        print('==== result_sent_back end ====')


if __name__ == '__main__':
    pass
