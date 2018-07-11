#!/usr/bin/env python3
# encoding: utf-8

from base_chain_node import BaseChainNode
import my_config
from contract_handler import ContractHandler
from chain_utils import convert_to_hex
from web3 import Web3
from oracle_core import OracleCore


class OracleNodeClient(BaseChainNode):

    def __init__(self,
                 config_path=my_config.CONFIG_PATH,
                 to_oracle_node_callback_objs=[],
                 wait_time=3):
        self._config_path = config_path
        self.to_oracle_node_callback_objs = [self] + to_oracle_node_callback_objs
        super(OracleNodeClient, self).__init__(config_path,
                                               wait_time)

    def to_oracle_node_event_callback(self, node, event):
        query_id = convert_to_hex(event['args']['queryId'])
        requests = event['args']['requests']
        print('in OracleNodeClient - event: query id {0}, requests {1}'.format(query_id, requests))
        response = 'show me the money'
        OracleCore(self._config_path).result_sent_back(query_id,
                                                       response,
                                                       convert_to_hex(Web3.sha3(text=response)))

    def setup_contract(self, config_path):
        all_events = OracleCore(config_path).get_all_events()
        return [{
            'contract_name': 'OracleCore',
            'event_name': 'ToOracleNode',
            'callback_objs': self.to_oracle_node_callback_objs,
            'callback_name': 'to_oracle_node_event_callback',
            'event_filter':
                all_events.ToOracleNode.createFilter(fromBlock='latest')
        }]


if __name__ == '__main__':
    chain_node = OracleNodeClient()
    chain_node.start()
    chain_node.join()
