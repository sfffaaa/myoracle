#!/usr/bin/env python3
# encoding: utf-8


import os
import json
from web3 import Web3
import hexbytes
from handler.config_handler import ConfigHandler
from utils.my_config import CONFIG_PATH


# User should implement compose_smart_contract_args + deploy_implement
class BaseDeployer():
    def __init__(self, config_path=CONFIG_PATH):
        self._config_path = config_path
        self._config_handler = ConfigHandler(config_path)
        self._oracle_owner = self._config_handler.get_oracle_owner()
        self._test_owner = self._config_handler.get_test_owner()

    def _compose_contract_build_path(self, truffle_build_path, target_contract_name):
        json_filename = '{0}.json'.format(target_contract_name)
        target_path = os.path.join(*[truffle_build_path, 'contracts', json_filename])
        return target_path

    def _get_build_contract_json_file_attribute(self, filepath, key):
        with open(filepath) as f:
            return json.load(f)[key]

    def _dump_contract_info(self, contract_path, contract_detail, contract_owner, file_path):
        file_path = os.path.abspath(file_path)
        dir_path = os.path.dirname(file_path)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        json_data = {
            'abi': self._get_build_contract_json_file_attribute(contract_path, 'abi'),
            'address': contract_detail['contractAddress'],
            'owner': contract_owner,
            'detail': {k: Web3.toHex(v) if type(v) is hexbytes.main.HexBytes else v
                       for k, v in contract_detail.items()}
        }
        with open(file_path, 'w') as f:
            json.dump(json_data, f)

    def _start_multiple_deploy_to_chain(self, contract_dict):
        contract_tx_hash = {}
        for contract_name, contract_inst in contract_dict.items():
            tx_hash = contract_inst.transact({'from': self._w3.eth.accounts[0]})
            contract_tx_hash[contract_name] = tx_hash

        tx_receipts = {contract_name: self._w3.eth.getTransactionReceipt(tx_hash)
                       for contract_name, tx_hash in contract_tx_hash.items()}
        self._w3.miner.start(1)
        tx_receipts = {
            contract_name: self._w3.eth.waitForTransactionReceipt(tx_hash,
                                                                  timeout=240)
            for contract_name, tx_hash in contract_tx_hash.items()
        }

        # self._w3.miner.stop()
        if None in tx_receipts.values():
            raise IOError('still cannot get contract result')

        return tx_receipts, self._w3.eth.accounts[0]

    def _get_contract_instance(self, contract_name):
        print('==== Deploy started {0} ===='.format(contract_name))
        build_path = self._config_handler.get_chain_config('Deploy', 'truffle_build_path')
        contract_path = self._compose_contract_build_path(build_path, contract_name)
        assert os.path.isfile(contract_path), 'file compiled path {0} doesn\'t exist'.format(contract_path)

        abi = self._get_build_contract_json_file_attribute(contract_path, 'abi')
        bytecode = self._get_build_contract_json_file_attribute(contract_path, 'bytecode')

        return self._w3.eth.contract(abi=abi, bytecode=bytecode)

    def _dump_multiple_smart_contract(self, contract_detail_dict, contract_owner):
        for contract_name, contract_detail in contract_detail_dict.items():
            build_path = self._config_handler.get_chain_config('Deploy', 'truffle_build_path')
            contract_path = self._compose_contract_build_path(build_path, contract_name)
            assert os.path.isfile(contract_path), 'file compiled path {0} doesn\'t exist'.format(contract_path)

            output_path = self._config_handler.get_chain_config('Output', 'file_path')
            output_path = os.path.join(output_path,
                                       '{0}.json'.format(contract_name))

            self._dump_contract_info(contract_path,
                                     contract_detail,
                                     contract_owner,
                                     output_path)

    def _show_multiple_smart_contract_detail(self, contract_detail_dict, contract_owner):
        for contract_name, contract_detail in contract_detail_dict.items():
            print('==== Deploy finished {0} ===='.format(contract_name))
            print('Contract detail:')
            for k, v in contract_detail.items():
                if type(v) is hexbytes.main.HexBytes:
                    print('    {0}: {1}'.format(k, Web3.toHex(v)))
                else:
                    print('    {0}: {1}'.format(k, v))
            print('Contract owner:')
            print('    owner: {0}'.format(contract_owner))

    def deploy_multiple_smart_contract(self, infos):
        contract_insts = {}
        for contract_name, my_args in infos.items():
            print('==== Deploy started {0} ===='.format(contract_name))
            my_args = self.compose_smart_contract_args(contract_name, my_args)

            contract_inst = self._get_contract_instance(contract_name)
            contract_inst = contract_inst.constructor(*my_args)
            contract_insts[contract_name] = contract_inst

        contract_detail_dict, contract_owner = self._start_multiple_deploy_to_chain(contract_insts)
        self._dump_multiple_smart_contract(contract_detail_dict, contract_owner)

        self._show_multiple_smart_contract_detail(contract_detail_dict, contract_owner)
        return contract_detail_dict

    def deploy(self):
        self._w3 = self._config_handler.get_web3()

        print('==== Compile smart contract ====')
        truffle_path = self._config_handler.get_chain_config('Deploy', 'truffle_path')
        cmd = '(cd {0}; truffle compile)'.format(truffle_path)
        print('run command {0}'.format(cmd))
        os.system(cmd)

        self.deploy_implement()

    def undeploy(self):
        ''' Actually, smart contract cannot undeploy, but I need an function to remove unused intermediate file'''
        contract_names = self._config_handler.get_all_contract_name()
        for contract_name in contract_names:
            contract_path = os.path.join(self._config_handler.get_chain_config('Output', 'file_path'),
                                         '{0}.json'.format(contract_name))
            if os.path.exists(contract_path):
                os.unlink(contract_path)

    # ===== You should change this =====
    def compose_smart_contract_args(self, contract_name, my_args):
        raise IOError('Child should implement it')

    def deploy_implement(self):
        raise IOError('Child should finish it')
