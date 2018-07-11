#!/usr/bin/env python3
# encoding: utf-8

from utils import my_config
from base_object.base_contract import BaseContract
from oracle_core_onchain_handler import OracleCoreOnChainHandler


class OracleCore(BaseContract):

    def __init__(self, config=my_config.CONFIG_PATH):
        super().__init__(config)

    def create_onchain_handler(self, config):
        return OracleCoreOnChainHandler(config)

    # --- Customize function for their onw function ---
    # This function should use in node, but I still implement it...
    def query_sent_node(self, address, requests):
        self._onchain_handler.query_sent_node(address, requests)

    def result_sent_back(self, query_id, response, hash_val):
        self._onchain_handler.result_sent_back(query_id, response, hash_val)


if __name__ == '__main__':
    OracleCore()
