#!/usr/bin/env python3
# encoding: utf-8

from utils import my_config
from base_object.base_contract import BaseContract
from oracle_register.oracle_register_onchain_handler import OracleRegisterOnChainHandler


class OracleRegister(BaseContract):

    def __init__(self, config=my_config.CONFIG_PATH):
        super().__init__(config)

    def create_onchain_handler(self, config):
        return OracleRegisterOnChainHandler(config)

    # --- Customize function for their onw function ---
    # This function should use in node, but I still implement it...
    def regist_address(self, name, address, **kargs):
        self._onchain_handler.regist_address(name, address, **kargs)

    def get_address(self, name, **kargs):
        return self._onchain_handler.get_address(name, **kargs)


if __name__ == '__main__':
    OracleRegister()
