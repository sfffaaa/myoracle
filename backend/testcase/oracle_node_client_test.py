#!/usr/bin/env python3
# encoding: utf-8

# import gevent
import unittest
import sys
sys.path.append('src')
from utils.my_deployer import MyDeployer
from clients.oracle_node_client import OracleNodeClient
from test_utils import _TEST_CONFIG
from oracle_core.oracle_core import OracleCore
from oracle_fee_wallet.oracle_fee_wallet import OracleFeeWallet
from test_oracle_example.test_oracle_example import TestOracleExample
from utils.chain_utils import convert_to_wei
import time
from gevent.event import Event


OVERHEAD_TIME = 15


def force_pass(arg):
    print("important_greelet pass")


def froce_die(arg):
    sys.exit("important_greenlet died")


class TestOracleNodeClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._callback_event = Event()
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
        self._callback_event.set()
        # fail if sent different request

    def test_single_late_event(self):
        self._callback_event.clear()
        TEST_TIME = 60
        private_daemon = OracleNodeClient(config_path=_TEST_CONFIG,
                                          to_oracle_node_callback_objs=[self],
                                          wait_time=1)
        private_daemon.link_exception(froce_die)
        private_daemon.start()

        test_example = TestOracleExample(_TEST_CONFIG)
        test_example.deposit(value=convert_to_wei(20000, 'wei'))

        oracle_fee_wallet = OracleFeeWallet(_TEST_CONFIG)
        before_balance = oracle_fee_wallet.get_balance(test_example.get_address())
        # use oracle_node to trigger event
        node = OracleCore(_TEST_CONFIG)
        node.query_sent_node(TEST_TIME,
                             test_example.get_address(),
                             'json(https://api.kraken.com/0/public/Ticker)["error"][0]')
        self._start_time = time.time()

        self._callback_event.wait()

        self.assertNotEqual(self._finish_time, 0, 'SHould not equal 0')
        self.assertTrue((self._finish_time - self._start_time) > TEST_TIME,
                        'callback should wait {0} - {1}'.format(self._finish_time, self._start_time))

        private_daemon.kill()
        self.assertEqual(self._tested, True, 'Should be tested')
        after_balance = oracle_fee_wallet.get_balance(test_example.get_address())
        self.assertEqual(before_balance, after_balance + 20000, 'Should be the same')

#    def test_single_immediately_success_event(self):
#        self._callback_event.clear()
#        TEST_TIME = 0
#        private_daemon = OracleNodeClient(config_path=_TEST_CONFIG,
#                                          to_oracle_node_callback_objs=[self],
#                                          wait_time=1)
#        private_daemon.link_exception(froce_die)
#        private_daemon.start()
#
#        # use oracle_node to trigger event
#        node = OracleCore(_TEST_CONFIG)
#        tx = node.query_sent_node(TEST_TIME,
#                                  '0xF2E246BB76DF876Cef8b38ae84130F4F55De395b',
#                                  'json(https://api.kraken.com/0/public/Ticker)["error"][0]')
#        self._start_time = time.time()
#
#        self._callback_event.wait()
#        self.assertNotEqual(self._finish_time, 0, 'SHould not equal 0')
#        check_time = self._finish_time - self._start_time
#        # Overtime will be influenced by cpu usage or other reason.
#        self.assertTrue(check_time < OVERHEAD_TIME,
#                        'callback should wait {0} < {1} (overhead_time)'.format(check_time, OVERHEAD_TIME))
#
#        private_daemon.kill()
#        self.assertEqual(self._tested, True, 'Should be tested')


if __name__ == '__main__':
    unittest.main()
