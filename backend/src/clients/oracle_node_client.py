#!/usr/bin/env python3
# encoding: utf-8

from base_object.base_chain_node import BaseChainNode
from utils import my_config
from utils.chain_utils import convert_to_hex
from web3 import Web3
from oracle_core.oracle_core import OracleCore
from handler.request_handler import RequestHandler
from utils.my_deployer import MyDeployer
import gevent


class OracleNodeClient(BaseChainNode):

    def __init__(self,
                 config_path=my_config.CONFIG_PATH,
                 to_oracle_node_callback_objs=[],
                 wait_time=3,
                 deployed=False,
                 deployed_event=None):
        if deployed:
            try:
                MyDeployer(config_path).undeploy()
            except IOError:
                pass
            else:
                raise
            MyDeployer(config_path).deploy()

        if deployed_event:
            deployed_event.set()

        self._config_path = config_path
        self.to_oracle_node_callback_objs = [self] + to_oracle_node_callback_objs

        super(OracleNodeClient, self).__init__(config_path,
                                               wait_time)

    def to_oracle_node_event_callback(self, node, event):
        timeout = int(event['args']['timeout'])
        query_id = convert_to_hex(event['args']['queryId'])
        request = event['args']['request']
        if timeout > 0:
            gevent.sleep(timeout)
        print('in OracleNodeClient - event: query id {0}, request {1}'.format(query_id, request))
        request_handler = RequestHandler(event['args']['request'])
        response = request_handler.execute_request()
        tx = OracleCore(self._config_path).result_sent_back(query_id,
                                                            response,
                                                            convert_to_hex(Web3.sha3(text=response)))
        print('Show tx after result back {0}'.format(tx))

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
