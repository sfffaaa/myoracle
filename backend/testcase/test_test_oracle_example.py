#!/usr/bin/env python3
# encoding: utf-8

import gevent
import unittest
import sys
sys.path.append('src')

from utils.my_deployer import MyDeployer
from clients.oracle_node_client import OracleNodeClient
from test_utils import _TEST_CONFIG
from test_oracle_example.test_oracle_example import TestOracleExample
from utils.chain_utils import convert_to_hex

TEST_REQUEST_STR = 'Show me the money'


class TestTestOracleExample(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        MyDeployer(_TEST_CONFIG).deploy()

    @classmethod
    def tearDownClass(cls):
        MyDeployer(_TEST_CONFIG).undeploy()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def to_oracle_node_event_callback(self, node, event):
        self.query_id = convert_to_hex(event['args']['queryId'])
        requests = event['args']['requests']
        self.assertEqual(requests, TEST_REQUEST_STR, 'Request should be the same')

    def test_single_event(self):
        private_daemon = OracleNodeClient(config_path=_TEST_CONFIG,
                                          to_oracle_node_callback_objs=[self],
                                          wait_time=1)
        private_daemon.start()

        test_example = TestOracleExample(_TEST_CONFIG)
        # self.assertEqual(0, test_example.get_lastest_query_id(), 'There is no query id')

        test_example.query_sent_node(TEST_REQUEST_STR)
        test_example_queryid = test_example.get_lastest_query_id()
        gevent.sleep(2)
        self.assertEqual(test_example_queryid, self.query_id, 'Two query id should be the same')

        # check the result is correct
        private_daemon.kill()


if __name__ == '__main__':
    unittest.main()
