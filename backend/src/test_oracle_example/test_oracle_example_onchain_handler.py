#!/usr/bin/env python3
# encoding: utf-8

from utils import my_config
from base_object.base_contract_onchain_handler import BaseContractOnChainHandler


class TestOracleExampleOnChainHandler(BaseContractOnChainHandler):

    def __init__(self, config_path=my_config.CONFIG_PATH):
        super().__init__(config_path)

    # --- implement base class ---
    def get_contract_handler_name(self):
        return 'TestOracleExample'

    # --- connect to contract function ---
    def trigger(self, **kargs):
        transaction_data = self.compose_transaction_dict(kargs)
        print('==== trigger start ====')
        tx_hash = self.get_contract_inst().functions.trigger() \
                                                    .transact(transaction_data)

        self.wait_miner_finish(tx_hash)
        print('==== trigger finish ====')

    def get_lastest_query_id(self, **kargs):
        transaction_data = self.compose_transaction_dict(kargs)
        print('==== get_lastest_query_id start ====')

        query_id = self.get_contract_inst().functions.getLastestQueryId().call(transaction_data)
        print('==== get_lastest_query_id end ====')
        return query_id


if __name__ == '__main__':
    pass
