#!/usr/bin/env python3
# encoding: utf-8

from utils import my_config
from base_object.base_contract_onchain_handler import BaseContractOnChainHandler


class OracleFeeWalletOnChainHandler(BaseContractOnChainHandler):

    def __init__(self, config_path=my_config.CONFIG_PATH):
        super().__init__(config_path)

    # --- connect to contract function ---
    def c_deposit(self, **kargs):
        transaction_data = self.compose_transaction_dict(kargs)
        tx_hash = self.get_contract_inst().functions.deposit() \
                                                    .transact(transaction_data)

        self.wait_miner_finish(tx_hash)
        return self._w3.eth.getTransactionReceipt(tx_hash)

    def c_payback(self, **kargs):
        transaction_data = self.compose_transaction_dict(kargs)
        tx_hash = self.get_contract_inst().functions.payback() \
                                                    .transact(transaction_data)

        self.wait_miner_finish(tx_hash)
        return self._w3.eth.getTransactionReceipt(tx_hash)

    def l_get_balance(self, address, **kargs):
        transaction_data = self.compose_transaction_dict(kargs)
        balance = self.get_contract_inst().functions.getBalance(address).call(transaction_data)
        return balance

    def c_register_client_addr(self, address, **kargs):
        transaction_data = self.compose_transaction_dict(kargs)
        tx_hash = self.get_contract_inst().functions.registerClientAddr(address) \
                                                    .transact(transaction_data)

        self.wait_miner_finish(tx_hash)
        return self._w3.eth.getTransactionReceipt(tx_hash)

    def c_register_multiple_client_addr(self, addresses, **kargs):
        transaction_data = self.compose_transaction_dict(kargs)
        tx_hashes = [self.get_contract_inst().functions.registerClientAddr(address)
                         .transact(transaction_data)
                     for address in addresses]

        self.wait_miner_finish(tx_hashes)
        return [self._w3.eth.getTransactionReceipt(tx_hash) for tx_hash in tx_hashes]


if __name__ == '__main__':
    pass
