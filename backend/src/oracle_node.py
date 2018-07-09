#!/usr/bin/env python3
# encoding: utf-8

import my_config
from oracle_node_onchain_handler import OracleNodeOnChainHandler


class OracleNode():

    def __init__(self, config=my_config.CONFIG_PATH):
        self._onchain_handler = OracleNodeOnChainHandler(config)

    # This function should use in node, but I still implement it...
    def querySentNode(self, address, requests):
        self._onchain_handler.querySentNode(address, requests)

    def resultSentBack(self, query_id, response, hash_val):
        self._onchain_handler.resultSentBack(query_id, response, hash_val)


if __name__ == '__main__':
    OracleNode()
