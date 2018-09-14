#!/usr/bin/env python3

from utils import my_config
from base_object.base_contract import BaseContract
from hodl_storage.hodl_storage_onchain_handler import HodlStorageOnChainHandler


class HodlStorage(BaseContract):

    def __init__(self, config=my_config.CONFIG_PATH):
        super().__init__(config)

    def create_onchain_handler(self, config):
        return HodlStorageOnChainHandler(config)


if __name__ == '__main__':
    HodlStorage()
