# !/usr/bin/env python3
# encoding: utf-8

from base_object.base_deployer import BaseDeployer
from oracle_storage.oracle_storage import OracleStorage
from oracle_register.oracle_register import OracleRegister


class MyDeployer(BaseDeployer):

    def deploy_implement(self, config_handler):

        # step 1
        info = self.deploy_multiple_smart_contract(config_handler, {
            'TestStorage': {},
            'OracleStorage': {},
        })
        contract_info = {}
        contract_info.update(info)

        # step 2
        info = self.deploy_multiple_smart_contract(config_handler, {
            'OracleRegister': contract_info,
        })
        contract_info.update(info)

        # step 3
        info = self.deploy_multiple_smart_contract(config_handler, {
            'OracleCore': contract_info,
            'TestOracleExample': contract_info,
        })
        contract_info.update(info)

        # final
        OracleStorage(self._config_path) \
            .set_oracle_register_addr(contract_info['OracleRegister']['contractAddress'])
        OracleRegister(self._config_path) \
            .regist_address('OracleCore',
                            contract_info['OracleCore']['contractAddress'])
        OracleRegister(self._config_path) \
            .regist_address('OracleStorage',
                            contract_info['OracleStorage']['contractAddress'])
        OracleRegister(self._config_path) \
            .regist_address('TestStorage',
                            contract_info['TestStorage']['contractAddress'])

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
        elif contract_name == 'TestStorage':
            return []
        else:
            raise IOError('Wrong contract name {0}'.format(contract_name))


if __name__ == '__main__':
    MyDeployer().deploy()
