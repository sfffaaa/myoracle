#!/usr/bin/env python3
# encoding: utf-8

from utils import my_config
from base_object.base_contract_onchain_handler import BaseContractOnChainHandler
from utils.chain_utils import convert_to_bytes, convert_to_hex


class OracleCoreOnChainHandler(BaseContractOnChainHandler):

    def __init__(self, config_path=my_config.CONFIG_PATH):
        super().__init__(config_path)

    # --- connect to contract function ---
    def c_set_oracle_core_addr(self, **kargs):
        transaction_data = self.compose_transaction_dict(kargs)
        tx_hash = self.get_contract_inst().functions.setOracleCoreAddr() \
                                                    .transact(transaction_data)

        self.wait_miner_finish(tx_hash)
        return convert_to_hex(tx_hash)

    def c_query_sent_node(self, timeout, address, requests, **kargs):
        transaction_data = self.compose_transaction_dict(kargs)
        tx_hash = self.get_contract_inst().functions.querySentNode(timeout, address, requests) \
                                                    .transact(transaction_data)

        self.wait_miner_finish(tx_hash)
        return convert_to_hex(tx_hash)

    def c_result_sent_back(self, query_id, response, hash_val, **kargs):
        transaction_data = self.compose_transaction_dict(kargs)

        tx_hash = self.get_contract_inst().functions.resultSentBack(convert_to_bytes(query_id),
                                                                    response,
                                                                    convert_to_bytes(hash_val)) \
                                                    .transact(transaction_data)
        self.wait_miner_finish(tx_hash)
        return convert_to_hex(tx_hash)


if __name__ == '__main__':
    pass
