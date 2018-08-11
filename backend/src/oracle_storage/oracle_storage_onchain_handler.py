#!/usr/bin/env python3
# encoding: utf-8

from utils import my_config
from base_object.base_contract_onchain_handler import BaseContractOnChainHandler
from utils.chain_utils import convert_to_hex


class OracleStorageOnChainHandler(BaseContractOnChainHandler):

    def __init__(self, config_path=my_config.CONFIG_PATH):
        super().__init__(config_path)

    # --- implement base class ---
    def get_contract_handler_name(self):
        return 'OracleStorage'

    # --- connect to contract function ---
    def c_set_oracle_register_addr(self, address, **kargs):
        transaction_data = self.compose_transaction_dict(kargs)
        print('==== set_oracle_register_addr start ====')
        tx_hash = self.get_contract_inst().functions.setOracleRegisterAddr(address) \
                                                    .transact(transaction_data)

        self.wait_miner_finish(tx_hash)
        print('==== set_oracle_register_addr finish ====')
        return convert_to_hex(tx_hash)


if __name__ == '__main__':
    pass
