#!/usr/bin/env python3
# encoding: utf-8

import gevent
import unittest
import sys
sys.path.append('src')

from utils.my_deployer import MyDeployer
from clients.oracle_node_client import OracleNodeClient
from clients.hodl_oracle_client import HodlOracleClient
from test_utils import _TEST_CONFIG
from hodl_oracle.hodl_oracle import HodlOracle
from utils.chain_utils import convert_to_hex, convert_to_wei
from handler.config_handler import ConfigHandler
from web3 import Web3

TEST_REQUEST_STR = 'json(https://api.kraken.com/0/public/Ticker)["error"][0]'
TEST_RESPONSE_STR = 'EGeneral:Invalid arguments'


class TestHodlOracle(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._hodl_owner = ConfigHandler(_TEST_CONFIG).get_hodl_owner()
        MyDeployer(_TEST_CONFIG).deploy()

    @classmethod
    def tearDownClass(cls):
        MyDeployer(_TEST_CONFIG).undeploy()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def to_oracle_node_event_callback(self, node, event):
        self.to_oracle_node_data.append({
            'queryId': convert_to_hex(event['args']['queryId']),
            'request': event['args']['request']
        })

    def sent_event_callback(self, node, event):
        self.sent_event_data.append({
            'queryId': convert_to_hex(event['args']['queryId']),
            'request': event['args']['request']
        })

    def show_event_callback(self, node, event):
        self.show_event_data.append({
            'queryId': convert_to_hex(event['args']['queryId']),
            'response': event['args']['response'],
            'hash': convert_to_hex(event['args']['hash'])
        })

    def test_single_event(self):
        self.to_oracle_node_data = []
        self.show_event_data = []
        self.sent_event_data = []
        example_daemon = HodlOracleClient(config_path=_TEST_CONFIG,
                                          sent_callback_objs=[self],
                                          show_callback_objs=[self],
                                          wait_time=1)
        example_daemon.start()

        node_daemon = OracleNodeClient(config_path=_TEST_CONFIG,
                                       to_oracle_node_callback_objs=[self],
                                       wait_time=1)
        node_daemon.start()

        hodl_oracle = HodlOracle(_TEST_CONFIG)
        # self.assertEqual(0, hodl_oracle.get_lastest_query_id(), 'There is no query id')

        hodl_oracle.deposit(**{
            'value': convert_to_wei(20000, 'wei'),
            'from': self._hodl_owner
        })
        hodl_oracle.trigger(**{
            'from': self._hodl_owner
        })
        hodl_oracle_queryid = hodl_oracle.get_lastest_query_id(**{
            'from': self._hodl_owner
        })
        gevent.sleep(5)

        for idx, test_list in enumerate([self.to_oracle_node_data, self.sent_event_data, self.show_event_data]):
            self.assertEqual(len(test_list),
                             1,
                             '{0} has more than one entry {1}'.format(test_list, idx))

        # check queryid
        for idx, test_list in enumerate([self.to_oracle_node_data, self.sent_event_data, self.show_event_data]):
            self.assertEqual(test_list[0]['queryId'],
                             hodl_oracle_queryid,
                             'query id {0} != {1}, {2}'.format(test_list[0]['queryId'],
                                                               hodl_oracle_queryid,
                                                               idx))

        # check resquest
        self.assertEqual(self.to_oracle_node_data[0]['request'],
                         self.sent_event_data[0]['request'],
                         'two request should be the same')

        # check response
        self.assertRegex(self.show_event_data[0]['response'], '^(\d+\.?\d+)$')

        self.assertEqual(convert_to_hex(self.show_event_data[0]['hash']),
                         convert_to_hex(Web3.sha3(text=self.show_event_data[0]['response'])))

        # check the result is correct
        example_daemon.kill()
        node_daemon.kill()


if __name__ == '__main__':
    unittest.main()
