#!/usr/bin/env python3
# encoding: utf-8

from utils import my_config
from utils.chain_utils import contract_function_log
from utils.fee_collector_utils import record_fee_client


class BaseContract():

    def __init__(self, config=my_config.CONFIG_PATH):
        self._onchain_handler = self.create_onchain_handler(config)
        self._expose_contract_function()

    def _expose_call_function(self):
        function_names = [function_name for function_name in dir(self._onchain_handler)
                          if function_name.startswith('l_') and
                          callable(getattr(self._onchain_handler, function_name))]

        for function_name in function_names:
            setattr(self,
                    function_name[2:],
                    contract_function_log(getattr(self._onchain_handler, function_name)))

    def _expose_transaction_function(self):
        function_names = [function_name for function_name in dir(self._onchain_handler)
                          if function_name.startswith('c_') and
                          callable(getattr(self._onchain_handler, function_name))]

        for function_name in function_names:
            setattr(self,
                    function_name[2:],
                    record_fee_client(self.__class__.__name__,
                                      function_name[2:],
                                      contract_function_log(getattr(self._onchain_handler, function_name))))

    def _expose_contract_function(self):
        self._expose_transaction_function()
        self._expose_call_function()

    def create_onchain_handler(self, config):
        raise IOError('Child should implement this function')

    def get_address(self):
        return self._onchain_handler.get_address()

    def get_balance(self):
        return self._onchain_handler.get_balance()

    def get_all_events(self):
        return self._onchain_handler.get_all_events()
