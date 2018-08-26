# !/usr/bin/env python3
# encoding: utf-8

from base_object.base_deployer import BaseDeployer
from oracle_storage.oracle_storage import OracleStorage
from test_storage.test_storage import TestStorage
from oracle_register.oracle_register import OracleRegister
import multiprocessing


class MyDeployer(BaseDeployer):

    def deploy_implement(self, config_handler):

        # step 1
        info = self.deploy_multiple_smart_contract(config_handler, {
            'OracleStorage': {},
            'OracleWallet': {},

            'TestStorage': {},
            # [TODO] Test Wallet doesn't use right now.
            'TestWallet': {},
        })
        contract_info = {}
        contract_info.update(info)

        # step 2
        info = self.deploy_multiple_smart_contract(config_handler, {
            'OracleRegister': contract_info,
            'TestWalletDistributor': contract_info,
        })
        contract_info.update(info)

        # step 3
        info = self.deploy_multiple_smart_contract(config_handler, {
            'OracleCore': contract_info,
            'TestOracleExample': contract_info,
        })
        contract_info.update(info)

        # final
        func_args_pairs = [
            (self._oracle_storage_register, contract_info),
            (self._oracle_register_register, contract_info),
            (self._test_stroage_allower, contract_info)
        ]
        procs = [multiprocessing.Process(target=func, args=(args,)) for func, args in func_args_pairs]
        for p in procs:
            p.start()
        for p in procs:
            p.join()

    def _oracle_storage_register(self, contract_info):
        OracleStorage(self._config_path) \
            .set_oracle_register_addr(contract_info['OracleRegister']['contractAddress'])

    def _oracle_register_register(self, contract_info):
        register_args = [('OracleCore', contract_info['OracleCore']['contractAddress']),
                         ('OracleStorage', contract_info['OracleStorage']['contractAddress']),
                         ('OracleWallet', contract_info['OracleWallet']['contractAddress']),
                         ('TestStorage', contract_info['TestStorage']['contractAddress']),
                         ('TestWalletDistributor', contract_info['TestWalletDistributor']['contractAddress'])]
        OracleRegister(self._config_path).regist_multiple_address(register_args)

    def _test_stroage_allower(self, contract_info):
        allower_args = [contract_info['TestWalletDistributor']['contractAddress'],
                        contract_info['TestOracleExample']['contractAddress']]
        TestStorage(self._config_path).set_multiple_allower(allower_args)

    def compose_smart_contract_args(self, config_handler, contract_name, my_args):
        if contract_name == 'OracleCore':
            return [self._w3.eth.accounts[0],
                    my_args['OracleRegister']['contractAddress']]
        elif contract_name == 'OracleStorage':
            return [self._w3.eth.accounts[0]]
        elif contract_name == 'OracleRegister':
            return [self._w3.eth.accounts[0],
                    my_args['OracleStorage']['contractAddress']]
        elif contract_name == 'TestOracleExample':
            return [self._w3.eth.accounts[0],
                    my_args['OracleRegister']['contractAddress']]
        elif contract_name == 'OracleWallet':
            return [self._w3.eth.accounts[0]]

        elif contract_name == 'TestStorage':
            return [self._w3.eth.accounts[0]]
        elif contract_name == 'TestWallet':
            return [self._w3.eth.accounts[0]]
        elif contract_name == 'TestWalletDistributor':
            return [my_args['TestStorage']['contractAddress']]
        else:
            raise IOError('Wrong contract name {0}'.format(contract_name))


if __name__ == '__main__':
    MyDeployer().deploy()
