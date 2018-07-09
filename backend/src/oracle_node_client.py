#!/usr/bin/env python3
# encoding: utf-8

from base_chain_node import BaseChainNode
import my_config
from contract_handler import ContractHandler
from chain_utils import convert_to_hex


class OracleNodeClient(BaseChainNode):

    def __init__(self,
                 config_path=my_config.CONFIG_PATH,
                 to_oracle_node_callback_objs=[],
                 wait_time=3):
        self.to_oracle_node_callback_objs = [self] + to_oracle_node_callback_objs
        super(OracleNodeClient, self).__init__(config_path,
                                               wait_time)

    def to_oracle_node_event_callback(self, node, event):
        query_id = event['args']['queryId']
        requests = event['args']['requests']
        print('in OracleNodeClient - event: query id {0}, requests {1}'.format(convert_to_hex(query_id),
                                                                               requests))

    def setup_contract(self, config_path):
        oracle_core_hdr = ContractHandler('OracleCore', config_path)
        return [{
            'contract_name': 'OracleCore',
            'event_name': 'ToOracleNode',
            'contract_handler': oracle_core_hdr,
            'callback_objs': self.to_oracle_node_callback_objs,
            'callback_name': 'to_oracle_node_event_callback',
            'event_filter':
                oracle_core_hdr._contract_inst.events.ToOracleNode.createFilter(fromBlock='latest')
        }]


if __name__ == '__main__':
    chain_node = OracleNodeClient()
    chain_node.start()
    chain_node.join()
