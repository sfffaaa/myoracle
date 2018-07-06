#!/usr/bin/env python3
# encoding: utf-8

from deployer_base import DeployerBase


class MyDeployer(DeployerBase):

    def DeployImplement(self, config_handler):

        # step 1
        step_one_info = self._DeployMultipleSmartContractV0(config_handler, {
            'OracleStorage': {},
            'TestOracleExample': {}
        })

        # step 2
        storage_info = step_one_info['OracleStorage']
        self._DeployMultipleSmartContractV0(config_handler, {
            'OracleCore': {'OracleStorage': storage_info}
        })

    def ComposeSmartContractArgs(self, config_handler, contract_name, my_args):
        if contract_name == 'OracleCore':
            return [my_args['OracleStorage']['contractAddress']]
        elif contract_name == 'OracleStorage':
            return []
        elif contract_name == 'TestOracleExample':
            return []
        else:
            raise IOError('Wrong contract name {0}'.format(contract_name))


if __name__ == '__main__':
    MyDeployer().deploy()
