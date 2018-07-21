#!/usr/bin/env python3
# encoding: utf-8

from utils import my_config
from base_object.base_contract_onchain_handler import BaseContractOnChainHandler
from utils.chain_utils import convert_to_hex


class OracleRegisterOnChainHandler(BaseContractOnChainHandler):

    def __init__(self, config_path=my_config.CONFIG_PATH):
        super().__init__(config_path)

    # --- implement base class ---
    def get_contract_handler_name(self):
        return 'OracleRegister'

    # --- connect to contract function ---
    def regist_address(self, name, address, **kargs):
        transaction_data = self.compose_transaction_dict(kargs)
        print('==== regist_address start ====')
        tx_hash = self.get_contract_inst().functions.registAddress(name, address) \
                                                    .transact(transaction_data)

        self.wait_miner_finish(tx_hash)
        print('==== regist_address finish ====')
        return convert_to_hex(tx_hash)

    def get_address(self, name, **kargs):
        transaction_data = self.compose_transaction_dict(kargs)
        print('==== get_address start ====')
        address = self.get_contract_inst().functions.getAddress(name).call(transaction_data)
        print('==== get_address finish ====')
        return convert_to_hex(address)


if __name__ == '__main__':
    pass
