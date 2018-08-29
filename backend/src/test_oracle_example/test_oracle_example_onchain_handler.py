#!/usr/bin/env python3
# encoding: utf-8

from utils import my_config
from base_object.base_contract_onchain_handler import BaseContractOnChainHandler
from utils.chain_utils import convert_to_hex


class TestOracleExampleOnChainHandler(BaseContractOnChainHandler):

    def __init__(self, config_path=my_config.CONFIG_PATH):
        super().__init__(config_path)

    # --- connect to contract function ---
    def c_trigger(self, **kargs):
        transaction_data = self.compose_transaction_dict(kargs)
        tx_hash = self.get_contract_inst().functions.trigger() \
                                                    .transact(transaction_data)

        self.wait_miner_finish(tx_hash)
        return convert_to_hex(tx_hash)

    def c_get_lastest_query_id(self, **kargs):
        transaction_data = self.compose_transaction_dict(kargs)

        query_id = self.get_contract_inst().functions.getLastestQueryId().call(transaction_data)
        return convert_to_hex(query_id)


if __name__ == '__main__':
    pass
