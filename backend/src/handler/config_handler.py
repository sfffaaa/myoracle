#!/usr/bin/env python3
# encoding: utf-8


import configparser
from utils.my_config import CONFIG_PATH
from web3 import Web3


class ConfigHandler():
    def __init__(self, config_path=CONFIG_PATH):
        self._config_path = config_path

    def get_chain_config(self, section, key):
        config = configparser.ConfigParser()
        config.read(self._config_path)
        return config.get(section, key)

    def get_web3(self):
        file_ipc = self.get_chain_config('Ethereum', 'file_ipc')
        return Web3(Web3.IPCProvider(file_ipc))
