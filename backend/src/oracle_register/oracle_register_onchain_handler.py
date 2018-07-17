#!/usr/bin/env python3
# encoding: utf-8

from utils import my_config
from base_object.base_contract_onchain_handler import BaseContractOnChainHandler
from utils.chain_utils import wait_miner, check_transaction_meet_assert, convert_to_hex


class OracleRegisterOnChainHandler(BaseContractOnChainHandler):

    def __init__(self, config_path=my_config.CONFIG_PATH):
        super().__init__(config_path)

    # --- implement base class ---
    def get_contract_handler_name(self):
        return 'OracleRegister'

    # --- connect to contract function ---
    def regist_address(self, name, address):
        w3 = self.get_w3_inst()
        print('==== regist_address start ====')
        tx_hash = self.get_contract_inst().functions.registAddress(name, address) \
                                                    .transact({'from': w3.eth.accounts[0],
                                                               'gas': my_config.GAS_SPENT})

        wait_miner(w3, tx_hash)
        if check_transaction_meet_assert(w3, tx_hash):
            raise IOError('assert encounter..')
        print('==== regist_address finish ====')

    def get_address(self, name):
        w3 = self.get_w3_inst()
        print('==== get_address start ====')
        address = self.get_contract_inst().functions.getAddress(name).call({'from': w3.eth.accounts[0]})
        print('==== get_address finish ====')
        return convert_to_hex(address)


if __name__ == '__main__':
    pass
