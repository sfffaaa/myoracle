#!/usr/bin/env python3
# encoding: utf-8

import gevent
import unittest
import sys
sys.path.append('src')
from utils.my_deployer import MyDeployer
from clients.oracle_node_client import OracleNodeClient
from test_utils import _TEST_CONFIG
from oracle_core.oracle_core import OracleCore


class TestOracleNodeClient(unittest.TestCase):

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
        # query_id = event['args']['queryId']
        requests = event['args']['requests']
        self.assertEqual(requests, 'show me the money')

    def test_single_event(self):
        private_daemon = OracleNodeClient(config_path=_TEST_CONFIG,
                                          to_oracle_node_callback_objs=[self],
                                          wait_time=1)
        private_daemon.start()

        # use oracle_node to trigger event
        node = OracleCore(_TEST_CONFIG)
        node.query_sent_node('0xF2E246BB76DF876Cef8b38ae84130F4F55De395b', 'show me the money')

        gevent.sleep(1)
        # check the result is correct
        private_daemon.kill()


if __name__ == '__main__':
    unittest.main()
