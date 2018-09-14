#!/usr/bin/env python3

from base_object.base_chain_node import BaseChainNode
from utils import my_config
from utils.chain_utils import convert_to_hex
from hodl_oracle.hodl_oracle import HodlOracle


class HodlOracleClient(BaseChainNode):

    def __init__(self,
                 config_path=my_config.CONFIG_PATH,
                 sent_callback_objs=[],
                 show_callback_objs=[],
                 wait_time=3):
        self._config_path = config_path
        self.sent_callback_objs = [self] + sent_callback_objs
        self.show_callback_objs = [self] + show_callback_objs
        super().__init__(config_path, wait_time)

    def sent_event_callback(self, node, event):
        query_id = convert_to_hex(event['args']['queryId'])
        data = event['args']['request']
        print('in HodlOracleClient(sent_event_callback) - event: query id {0}, data {1}'.format(query_id, data))

    def show_event_callback(self, node, event):
        query_id = convert_to_hex(event['args']['queryId'])
        response = event['args']['response']
        hash_resp = convert_to_hex(event['args']['hash'])
        print('in HodlOracleClient(show_event_callback) - event: query id {0}, hash {1}, response {2}'
              .format(query_id, hash_resp, response))

    def setup_contract(self, config_path):
        all_events = HodlOracle(config_path).get_all_events()
        return [{
            'contract_name': 'HodlOracle',
            'event_name': 'SentCallback',
            'callback_objs': self.sent_callback_objs,
            'callback_name': 'sent_event_callback',
            'event_filter': all_events.SentCallback.createFilter(fromBlock='latest')
        }, {
            'contract_name': 'HodlOracle',
            'event_name': 'ShowCallback',
            'callback_objs': self.show_callback_objs,
            'callback_name': 'show_event_callback',
            'event_filter': all_events.ShowCallback.createFilter(fromBlock='latest')
        }]


if __name__ == '__main__':
    chain_node = HodlOracleClient()
    chain_node.start()
    chain_node.join()
