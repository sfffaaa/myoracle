#!/usr/bin/env python3
# encoding: utf-8


import configparser
from utils.my_config import CONFIG_PATH
from web3 import Web3
import os


class ConfigHandler():
    def __init__(self, config_path=CONFIG_PATH):
        self._config_path = config_path
        self._config = configparser.ConfigParser()
        self._config.read(self._config_path)

    def get_chain_config(self, section, key):
        return self._config.get(section, key)

    def get_all_contract_name(self):
        contract_path = self.get_chain_config('Deploy', 'truffle_build_path')
        contract_path = os.path.join(contract_path, 'contracts')
        filenames = [f.split('.')[0] for f in os.listdir(contract_path)]
        filenames = [f for f in filenames if f != 'Migrations']
        return filenames

    def get_hodl_owner(self):
        owner_account = self.get_chain_config('Deploy', 'hodl_owner')
        if not owner_account:
            owner_account = self.get_web3().eth.accounts[2]
        return owner_account

    def get_oracle_owner(self):
        owner_account = self.get_chain_config('Deploy', 'oracle_owner')
        if not owner_account:
            owner_account = self.get_web3().eth.accounts[1]
        return owner_account

    def get_web3(self):
        keys = ['file_ipc', 'socket_ipc']
        ipc_configs = [self.get_chain_config('Ethereum', key) for key in keys
                       if self._config.has_option('Ethereum', key)]
        ipc_configs = [ipc_config for ipc_config in ipc_configs if ipc_config]
        if not len(ipc_configs):
            raise IOError("keys[{0}] doesn't have data".format(','.join(keys)))
        return Web3(Web3.IPCProvider(ipc_configs[0]))
