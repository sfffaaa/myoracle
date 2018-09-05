#!/usr/bin/env python3
# encoding: utf-8

from utils import my_config
from base_object.base_contract import BaseContract
from hodl_oracle.hodl_oracle_onchain_handler import HodlOracleOnChainHandler


class HodlOracle(BaseContract):

    def __init__(self, config=my_config.CONFIG_PATH):
        super().__init__(config)

    def create_onchain_handler(self, config):
        return HodlOracleOnChainHandler(config)


if __name__ == '__main__':
    pass
