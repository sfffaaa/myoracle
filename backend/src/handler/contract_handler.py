from utils import my_config
from handler.config_handler import ConfigHandler
import os
import json


class ContractHandler():

    def __init__(self, contract_name, config_path=my_config.CONFIG_PATH):
        self._config_handler = ConfigHandler(config_path)

        self._check_contract_name(contract_name)
        self._w3 = self._config_handler.get_web3()

        contract_info = self._get_contract_info(contract_name)
        contract_abi = contract_info['abi']
        self._contract_address = contract_info['address']
        self._contract_inst = self._w3.eth.contract(self._contract_address,
                                                    abi=contract_abi)

    def _check_contract_name(self, check_name):
        contract_path = self._config_handler.get_chain_config('Deploy', 'truffle_build_path')
        contract_path = os.path.join(contract_path, 'contracts')
        filenames = [f.split('.')[0] for f in os.listdir(contract_path)]
        filenames = [f for f in filenames if f != 'Migrations']
        if check_name not in filenames:
            raise IOError('Cannot find {0} in config {1}'.format(check_name, filenames))

    def get_address(self):
        return self._contract_address

    def get_w3(self):
        return self._w3

    def get_balance(self):
        return self._w3.eth.getBalance(self._contract_address)

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
