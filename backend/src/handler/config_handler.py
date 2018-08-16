#!/usr/bin/env python3
# encoding: utf-8


import configparser
from utils.my_config import CONFIG_PATH
from web3 import Web3


class ConfigHandler():
    def __init__(self, config_path=CONFIG_PATH):
        self._config_path = config_path
        self._config = configparser.ConfigParser()
        self._config.read(self._config_path)

    def get_chain_config(self, section, key):
        return self._config.get(section, key)

    def get_web3(self):
        keys = ['file_ipc', 'socket_ipc']
        ipc_configs = [self.get_chain_config('Ethereum', key) for key in keys
                       if self._config.has_option('Ethereum', key)]
        ipc_configs = [ipc_config for ipc_config in ipc_configs if ipc_config]
        if not len(ipc_configs):
            raise IOError("keys[{0}] doesn't have data".format(','.join(keys)))
        return Web3(Web3.IPCProvider(ipc_configs[0]))
