#!/usr/bin/env python3
# encoding: utf-8

from utils import my_config
from utils.chain_utils import convert_to_hex
from base_object.base_contract_onchain_handler import BaseContractOnChainHandler


class TestWalletDistributorOnChainHandler(BaseContractOnChainHandler):

    def __init__(self, config_path=my_config.CONFIG_PATH):
        super().__init__(config_path)

    # --- implement base class ---
    def get_contract_handler_name(self):
        return 'TestWalletDistributor'

    # --- connect to contract function ---
    def c_deposit_balance(self, address, **kargs):
        transaction_data = self.compose_transaction_dict(kargs)
        print('==== deposit_balance start ====')
        tx_hash = self.get_contract_inst().functions.depositBalance(address) \
                                                    .transact(transaction_data)

        self.wait_miner_finish(tx_hash)
        print('==== deposit_balance finish ====')
        return convert_to_hex(tx_hash)

    def c_withdraw_balance(self, address, **kargs):
        transaction_data = self.compose_transaction_dict(kargs)
        print('==== withdraw_balance start ====')
        tx_hash = self.get_contract_inst().functions.withdrawBalance(address) \
                                                    .transact(transaction_data)

        self.wait_miner_finish(tx_hash)
        print('==== withdraw_balance finish ====')
        return convert_to_hex(tx_hash)


if __name__ == '__main__':
    pass
