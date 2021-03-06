#!/usr/bin/env python3
# encoding: utf-8

from utils import my_config
from base_object.base_contract_onchain_handler import BaseContractOnChainHandler


class OracleStorageOnChainHandler(BaseContractOnChainHandler):

    def __init__(self, config_path=my_config.CONFIG_PATH):
        super().__init__(config_path)

    # --- connect to contract function ---
    def c_set_oracle_register_addr(self, address, **kargs):
        transaction_data = self.compose_transaction_dict(kargs)
        tx_hash = self.get_contract_inst().functions.setOracleRegisterAddr(address) \
                                                    .transact(transaction_data)

        self.wait_miner_finish(tx_hash)
        return self._w3.eth.getTransactionReceipt(tx_hash)


if __name__ == '__main__':
    pass
