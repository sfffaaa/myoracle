#!/usr/bin/env python3
# encoding: utf-8

from utils import my_config
from base_object.base_contract import BaseContract
from oracle_core.oracle_core_onchain_handler import OracleCoreOnChainHandler


class OracleCore(BaseContract):

    def __init__(self, config=my_config.CONFIG_PATH):
        super().__init__(config)

    def create_onchain_handler(self, config):
        return OracleCoreOnChainHandler(config)


if __name__ == '__main__':
    OracleCore()
