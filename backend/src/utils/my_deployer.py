#!/usr/bin/env python3
# encoding: utf-8

from base_object.base_deployer import BaseDeployer
from oracle_storage.oracle_storage import OracleStorage
from oracle_register.oracle_register import OracleRegister


class MyDeployer(BaseDeployer):

    def deploy_implement(self, config_handler):

        # step 1
        step_one_info = self.deploy_multiple_smart_contract(config_handler, {
            'TestStorage': {},
            'OracleStorage': {},
        })
        # step 2
        storage_info = {
            'OracleStorage': step_one_info['OracleStorage'],
            'TestStorage': step_one_info['TestStorage']
        }
        oracle_info = self.deploy_multiple_smart_contract(config_handler, {
            'OracleCore': {'OracleStorage': storage_info['OracleStorage']},
            'OracleRegister': {'OracleStorage': storage_info['OracleStorage']},
        })
        self.deploy_multiple_smart_contract(config_handler, {
            'TestOracleExample': {'OracleRegister': oracle_info['OracleRegister'],
                                  'TestStorage': storage_info['TestStorage']},
        })

        OracleStorage(self._config_path) \
            .set_oracle_register_addr(oracle_info['OracleRegister']['contractAddress'])
        OracleRegister(self._config_path) \
            .regist_address('OracleCore',
                            oracle_info['OracleCore']['contractAddress'])

    def compose_smart_contract_args(self, config_handler, contract_name, my_args):
        if contract_name == 'OracleCore':
            return [self._w3.eth.accounts[0],
                    my_args['OracleStorage']['contractAddress']]
        elif contract_name == 'OracleStorage':
            return [self._w3.eth.accounts[0]]
        elif contract_name == 'OracleRegister':
            return [self._w3.eth.accounts[0],
                    my_args['OracleStorage']['contractAddress']]
        elif contract_name == 'TestOracleExample':
            return [self._w3.eth.accounts[0],
                    my_args['OracleRegister']['contractAddress'],
                    my_args['TestStorage']['contractAddress']]
        elif contract_name == 'TestStorage':
            return []
        else:
            raise IOError('Wrong contract name {0}'.format(contract_name))


if __name__ == '__main__':
    MyDeployer().deploy()
