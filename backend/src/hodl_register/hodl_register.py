#!/usr/bin/env python3

from utils import my_config
from base_object.base_contract import BaseContract
from hodl_register.hodl_register_onchain_handler import HodlRegisterOnChainHandler


class HodlRegister(BaseContract):

    def __init__(self, config=my_config.CONFIG_PATH):
        super().__init__(config)

    def create_onchain_handler(self, config):
        return HodlRegisterOnChainHandler(config)


if __name__ == '__main__':
    HodlRegister()
