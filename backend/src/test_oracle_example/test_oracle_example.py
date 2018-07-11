#!/usr/bin/env python3
# encoding: utf-8

from utils import my_config
from base_object.base_contract import BaseContract
from test_oracle_example.test_oracle_example_onchain_handler import TestOracleExampleOnChainHandler
from utils.chain_utils import convert_to_hex


class TestOracleExample(BaseContract):

    def __init__(self, config=my_config.CONFIG_PATH):
        super().__init__(config)

    def create_onchain_handler(self, config):
        return TestOracleExampleOnChainHandler(config)

    # --- Customize function for their onw function ---
    # This function should use in node, but I still implement it...
    def query_sent_node(self, data):
        self._onchain_handler.query_sent_node(data)

    def get_lastest_query_id(self):
        b_queryid = self._onchain_handler.get_lastest_query_id()
        return convert_to_hex(b_queryid)


if __name__ == '__main__':
    pass
