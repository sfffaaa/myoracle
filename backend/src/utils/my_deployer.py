# !/usr/bin/env python3
# encoding: utf-8

from base_object.base_deployer import BaseDeployer
from oracle_storage.oracle_storage import OracleStorage
from oracle_register.oracle_register import OracleRegister
from oracle_fee_wallet.oracle_fee_wallet import OracleFeeWallet

from test_storage.test_storage import TestStorage
from hodl_register.hodl_register import HodlRegister
import multiprocessing


class MyDeployer(BaseDeployer):

    def deploy_implement(self):

        # step 1
        info = self.deploy_multiple_smart_contract({
            'OracleStorage': {},
            'OracleFeeWallet': {},

            'TestStorage': {},
        })
        contract_info = {}
        contract_info.update(info)

        # step 2
        info = self.deploy_multiple_smart_contract({
            'OracleRegister': contract_info,
            'HodlRegister': contract_info,
        })
        contract_info.update(info)

        # step 3
        info = self.deploy_multiple_smart_contract({
            'OracleWallet': contract_info,
            'OracleCore': contract_info,
            'TestWalletDistributor': contract_info,
            'TestOracleExample': contract_info,
        })
        contract_info.update(info)

        # step 4
        self._oracle_storage_register(contract_info)

        # step 5 (because it has dependency)
        func_args_pairs = [
            (self._oracle_register_register, contract_info),
            (self._hodl_register_register, contract_info),
            (self._test_stroage_allower, contract_info),
            (self._oracle_fee_wallet_register, contract_info),
        ]
        procs = [multiprocessing.Process(target=func, args=(args,)) for func, args in func_args_pairs]
        for p in procs:
            p.start()
        for p in procs:
            p.join()

    def _oracle_storage_register(self, contract_info):
        OracleStorage(self._config_path) \
            .set_oracle_register_addr(contract_info['OracleRegister']['contractAddress'], **{
                'from': self._oracle_owner
            })

    def _oracle_register_register(self, contract_info):
        register_args = [('OracleCore', contract_info['OracleCore']['contractAddress']),
                         ('OracleStorage', contract_info['OracleStorage']['contractAddress']),
                         ('OracleWallet', contract_info['OracleWallet']['contractAddress']),
                         ('OracleFeeWallet', contract_info['OracleFeeWallet']['contractAddress'])]
        OracleRegister(self._config_path).regist_multiple_address(register_args, **{
            'from': self._oracle_owner
        })

    def _hodl_register_register(self, contract_info):
        register_args = [('TestStorage', contract_info['TestStorage']['contractAddress']),
                         ('TestWalletDistributor', contract_info['TestWalletDistributor']['contractAddress']),
                         ('TestOracleExample', contract_info['TestOracleExample']['contractAddress'])]
        HodlRegister(self._config_path).regist_multiple_address(register_args, **{
            'from': self._test_owner,
        })

    def _test_stroage_allower(self, contract_info):
        allower_args = [contract_info['TestWalletDistributor']['contractAddress'],
                        contract_info['TestOracleExample']['contractAddress']]
        TestStorage(self._config_path).set_multiple_allower(allower_args, **{
            'from': self._test_owner
        })

    def _oracle_fee_wallet_register(self, contract_info):
        addresses = [contract_info['OracleWallet']['contractAddress']]
        OracleFeeWallet(self._config_path).register_multiple_client_addr(addresses, **{
            'from': self._oracle_owner
        })

    def compose_smart_contract_args(self, contract_name, my_args):
        if contract_name == 'OracleCore':
            return [self._oracle_owner,
                    my_args['OracleRegister']['contractAddress']]
        elif contract_name == 'OracleStorage':
            return [self._oracle_owner]
        elif contract_name == 'OracleRegister':
            return [self._oracle_owner]
        elif contract_name == 'OracleWallet':
            return [self._oracle_owner,
                    my_args['OracleRegister']['contractAddress']]
        elif contract_name == 'OracleFeeWallet':
            return [self._oracle_owner]

        elif contract_name == 'TestStorage':
            return [self._test_owner]
        elif contract_name == 'HodlRegister':
            return [self._test_owner]
        elif contract_name == 'TestWalletDistributor':
            return [self._test_owner,
                    my_args['HodlRegister']['contractAddress']]

        elif contract_name == 'TestOracleExample':
            return [self._test_owner,
                    my_args['OracleRegister']['contractAddress'],
                    my_args['HodlRegister']['contractAddress']]

        else:
            raise IOError('Wrong contract name {0}'.format(contract_name))


if __name__ == '__main__':
    MyDeployer().deploy()
