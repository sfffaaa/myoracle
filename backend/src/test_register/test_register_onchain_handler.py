#!/usr/bin/env python3
# encoding: utf-8

from utils import my_config
from base_object.base_contract_onchain_handler import BaseContractOnChainHandler
from utils.chain_utils import convert_to_hex


class TestRegisterOnChainHandler(BaseContractOnChainHandler):

    def __init__(self, config_path=my_config.CONFIG_PATH):
        super().__init__(config_path)

    # --- connect to contract function ---
    def c_regist_address(self, name, address, **kargs):
        transaction_data = self.compose_transaction_dict(kargs)
        tx_hash = self.get_contract_inst().functions.registAddress(name, address) \
                                                    .transact(transaction_data)

        self.wait_miner_finish(tx_hash)
        return convert_to_hex(tx_hash)

    def c_regist_multiple_address(self, address_pairs, **kargs):
        transaction_data = self.compose_transaction_dict(kargs)
        tx_hashes = [self.get_contract_inst().functions.registAddress(name, address)
                         .transact(transaction_data)
                     for name, address in address_pairs]

        self.wait_miner_finish(tx_hashes)
        return [convert_to_hex(tx_hash) for tx_hash in tx_hashes]

    def c_get_address(self, name, **kargs):
        transaction_data = self.compose_transaction_dict(kargs)
        address = self.get_contract_inst().functions.getAddress(name).call(transaction_data)
        return convert_to_hex(address)


if __name__ == '__main__':
    pass
