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
from utils.chain_utils import convert_to_wei
import time


OVERHEAD_TIME = 5


def force_pass(arg):
    print("important_greelet pass")


def froce_die(arg):
    sys.exit("important_greenlet died")


class TestOracleNodeClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        MyDeployer(_TEST_CONFIG).deploy()

    @classmethod
    def tearDownClass(cls):
        MyDeployer(_TEST_CONFIG).undeploy()

    def setUp(self):
        self._tested = False
        self._finish_time = 0
        pass

    def tearDown(self):
        pass

    def to_oracle_node_event_callback(self, node, event):
        self._tested = True
        self._finish_time = time.time()
        # query_id = event['args']['queryId']
        requests = event['args']['request']
        self.assertEqual(requests, 'json(https://api.kraken.com/0/public/Ticker)["error"][0]')
        # fail if sent different request

    def test_single_late_event(self):
        TEST_TIME = 60
        private_daemon = OracleNodeClient(config_path=_TEST_CONFIG,
                                          to_oracle_node_callback_objs=[self],
                                          wait_time=1)
        private_daemon.link_exception(froce_die)
        private_daemon.start()

        # use oracle_node to trigger event
        node = OracleCore(_TEST_CONFIG)
        node.query_sent_node(TEST_TIME,
                             '0xF2E246BB76DF876Cef8b38ae84130F4F55De395b',
                             'json(https://api.kraken.com/0/public/Ticker)["error"][0]',
                             value=convert_to_wei(1000, 'wei'))
        self._start_time = time.time()

        for _ in range(TEST_TIME * 2):
            gevent.sleep(1)
        self.assertTrue((self._finish_time - self._start_time) > TEST_TIME, 'callback should wait')

        private_daemon.kill()
        self.assertEqual(self._tested, True, 'Should be tested')

    def test_single_immediately_success_event(self):
        TEST_TIME = 0
        private_daemon = OracleNodeClient(config_path=_TEST_CONFIG,
                                          to_oracle_node_callback_objs=[self],
                                          wait_time=1)
        private_daemon.link_exception(froce_die)
        private_daemon.start()

        # use oracle_node to trigger event
        node = OracleCore(_TEST_CONFIG)
        node.query_sent_node(TEST_TIME,
                             '0xF2E246BB76DF876Cef8b38ae84130F4F55De395b',
                             'json(https://api.kraken.com/0/public/Ticker)["error"][0]',
                             value=convert_to_wei(1000, 'wei'))
        self._start_time = time.time()

        for _ in range(2):
            gevent.sleep(1)
        self.assertTrue((self._finish_time - self._start_time) < OVERHEAD_TIME, 'callback should wait')

        private_daemon.kill()
        self.assertEqual(self._tested, True, 'Should be tested')


if __name__ == '__main__':
    unittest.main()
