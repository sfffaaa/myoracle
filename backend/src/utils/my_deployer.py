#!/usr/bin/env python3
# encoding: utf-8

from base_object.base_deployer import BaseDeployer


class MyDeployer(BaseDeployer):

    def deploy_implement(self, config_handler):

        # step 1
        step_one_info = self.deploy_multiple_smart_contract(config_handler, {
            'OracleStorage': {},
        })

        # step 2
        storage_info = step_one_info['OracleStorage']
        self.deploy_multiple_smart_contract(config_handler, {
            'OracleCore': {'OracleStorage': storage_info},
            'TestOracleExample': {'OracleStorage': storage_info}
        })

    def compose_smart_contract_args(self, config_handler, contract_name, my_args):
        if contract_name == 'OracleCore':
            return [self._w3.eth.accounts[0], my_args['OracleStorage']['contractAddress']]
        elif contract_name == 'OracleStorage':
            return []
        elif contract_name == 'TestOracleExample':
            return [self._w3.eth.accounts[0], my_args['OracleStorage']['contractAddress']]
        else:
            raise IOError('Wrong contract name {0}'.format(contract_name))


if __name__ == '__main__':
    MyDeployer().deploy()
