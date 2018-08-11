#!/usr/bin/env python3
# encoding: utf-8

from utils import my_config
from base_object.base_contract import BaseContract
from oracle_storage.oracle_storage_onchain_handler import OracleStorageOnChainHandler


class OracleStorage(BaseContract):

    def __init__(self, config=my_config.CONFIG_PATH):
        super().__init__(config)

    def create_onchain_handler(self, config):
        return OracleStorageOnChainHandler(config)


if __name__ == '__main__':
    OracleStorage()
