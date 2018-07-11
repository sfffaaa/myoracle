#!/usr/bin/env python3
# encoding: utf-8

import my_config
from contract_handler import ContractHandler


class BaseContractOnChainHandler():

    def __init__(self, config_path=my_config.CONFIG_PATH):
        contract_name = self.get_contract_handler_name()
        self._contract_handler = ContractHandler(contract_name, config_path)
        self._w3 = self._contract_handler.get_w3()
        self._contract_inst = self._contract_handler.get_contract()

    def get_w3_inst(self):
        return self._w3

    def get_contract_inst(self):
        return self._contract_inst

    def get_all_events(self):
        return self._contract_handler.get_all_events()

    def get_contract_handler_name(self):
        raise IOError('Child should implement it')
