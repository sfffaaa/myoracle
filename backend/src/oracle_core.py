#!/usr/bin/env python3
# encoding: utf-8

import my_config
from oracle_core_onchain_handler import OracleCoreOnChainHandler


class OracleCore():

    def __init__(self, config=my_config.CONFIG_PATH):
        self._onchain_handler = OracleCoreOnChainHandler(config)

    def get_all_events(self):
        return self._onchain_handler.get_all_events()

    # This function should use in node, but I still implement it...
    def query_sent_node(self, address, requests):
        self._onchain_handler.query_sent_node(address, requests)

    def result_sent_back(self, query_id, response, hash_val):
        self._onchain_handler.result_sent_back(query_id, response, hash_val)


if __name__ == '__main__':
    OracleCore()
