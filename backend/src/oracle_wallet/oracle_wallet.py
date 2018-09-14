#!/usr/bin/env python3

from utils import my_config
from base_object.base_contract import BaseContract
from oracle_wallet.oracle_wallet_onchain_handler import OracleWalletOnChainHandler


class OracleWallet(BaseContract):

    def __init__(self, config=my_config.CONFIG_PATH):
        super().__init__(config)

    def create_onchain_handler(self, config):
        return OracleWalletOnChainHandler(config)


if __name__ == '__main__':
    OracleWallet()
