#!/usr/bin/env python3
# encoding: utf-8

from utils import my_config
from handler.contract_handler import ContractHandler
from utils.chain_utils import wait_miner, check_tx_receipts_meet_assert


class BaseContractOnChainHandler():

    def __init__(self, config_path=my_config.CONFIG_PATH):
        contract_name = self._get_contract_handler_name()
        self._contract_handler = ContractHandler(contract_name, config_path)
        self._w3 = self._contract_handler.get_w3()
        self._contract_inst = self._contract_handler.get_contract()

    def _get_contract_handler_name(self):
        suffix = 'OnChainHandler'
        class_name = self.__class__.__name__
        if not class_name.endswith(suffix):
            raise IOError('Naming rule is not suitable {0}, lack of {1}'.format(class_name, suffix))
        return class_name[:len(class_name) - len(suffix)]

    def compose_transaction_dict(self, kargs):
        default_data = {
            'from': self.get_w3_inst().eth.accounts[0],
            'gas': my_config.GAS_SPENT
        }
        default_data.update(kargs)
        return default_data

    def get_address(self):
        return self._contract_handler.get_address()

    def get_balance(self):
        return self._contract_handler.get_balance()

    def get_w3_inst(self):
        return self._w3

    def get_contract_inst(self):
        return self._contract_inst

    def get_all_events(self):
        return self._contract_handler.get_all_events()

    def get_contract_handler_name(self):
        raise IOError('Child should implement it')

    def wait_miner_finish(self, tx_hash):
        w3 = self.get_w3_inst()
        tx_receipts = wait_miner(w3, tx_hash)
        if check_tx_receipts_meet_assert(tx_receipts):
            raise IOError('assert encounter..')
