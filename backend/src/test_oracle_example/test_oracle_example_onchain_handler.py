#!/usr/bin/env python3
# encoding: utf-8

from utils import my_config
from base_object.base_contract_onchain_handler import BaseContractOnChainHandler
from utils.chain_utils import wait_miner, check_transaction_meet_assert


class TestOracleExampleOnChainHandler(BaseContractOnChainHandler):

    def __init__(self, config_path=my_config.CONFIG_PATH):
        super().__init__(config_path)

    # --- implement base class ---
    def get_contract_handler_name(self):
        return 'TestOracleExample'

    # --- connect to contract function ---
    def query_sent_node(self, request):
        w3 = self.get_w3_inst()
        print('==== query_sent_node start ====')
        tx_hash = self.get_contract_inst().functions.querySentNode(request) \
                                                    .transact({'from': w3.eth.accounts[0],
                                                               'gas': my_config.GAS_SPENT})

        wait_miner(w3, tx_hash)
        if check_transaction_meet_assert(w3, tx_hash):
            raise IOError('assert encounter..')
        print('==== query_sent_node finish ====')

    def get_lastest_query_id(self):
        print('==== get_lastest_query_id start ====')

        query_id = self.get_contract_inst().functions.getLastestQueryId().call()
        print('==== get_lastest_query_id end ====')
        return query_id


if __name__ == '__main__':
    pass
