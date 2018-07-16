#!/usr/bin/env python3
# encoding: utf-8

from utils import my_config
from base_object.base_contract_onchain_handler import BaseContractOnChainHandler
from utils.chain_utils import convert_to_bytes, wait_miner, check_transaction_meet_assert


class OracleStorageOnChainHandler(BaseContractOnChainHandler):

    def __init__(self, config_path=my_config.CONFIG_PATH):
        super().__init__(config_path)

    # --- implement base class ---
    def get_contract_handler_name(self):
        return 'OracleStorage'

    # --- connect to contract function ---
    def set_oracle_core_addr(self, address):
        w3 = self.get_w3_inst()
        print('==== set_oracle_core_addr start ====')
        tx_hash = self.get_contract_inst().functions.setOracleCoreAddr(address) \
                                                    .transact({'from': w3.eth.accounts[0],
                                                               'gas': my_config.GAS_SPENT})

        wait_miner(w3, tx_hash)
        if check_transaction_meet_assert(w3, tx_hash):
            raise IOError('assert encounter..')
        print('==== set_oracle_core_addr finish ====')


if __name__ == '__main__':
    pass
