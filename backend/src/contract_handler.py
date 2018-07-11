import my_config
from web3 import Web3
from config_handler import ConfigHandler
import os
import json


class ContractHandler():

    def __init__(self, contract_name, config_path=my_config.CONFIG_PATH):
        self._config_handler = ConfigHandler(config_path)

        self._check_contract_name(contract_name)

        file_ipc = self._config_handler.get_chain_config('Ethereum', 'file_ipc')
        self._w3 = Web3(Web3.IPCProvider(file_ipc))

        contract_info = self._get_contract_info(contract_name)
        contract_abi = contract_info['abi']
        contract_address = contract_info['address']
        self._contract_inst = self._w3.eth.contract(contract_address,
                                                    abi=contract_abi)

    def _check_contract_name(self, check_name):
        contract_names = self._config_handler.get_chain_config('Deploy', 'target_contract_name')
        if check_name not in contract_names.split(','):
            raise IOError('Cannot find {0} in config {1}'.format(check_name, contract_names))

    def get_w3(self):
        return self._w3

    def get_contract(self):
        return self._contract_inst

    def get_all_events(self):
        return self._contract_inst.events

    def _get_contract_info(self, contract_name):
        file_path = os.path.join(self._config_handler.get_chain_config('Output', 'file_path'),
                                 '{0}.json'.format(contract_name))
        file_path = os.path.abspath(file_path)
        with open(file_path) as f:
            contract_info = json.load(f)
        return contract_info
