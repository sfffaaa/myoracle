#!/usr/bin/env python3
# encoding: utf-8

import unittest
import sys
import multiprocessing
sys.path.append('src')

from utils.my_deployer import MyDeployer
from test_utils import _TEST_CONFIG, get_eth_price
from utils.chain_utils import convert_to_wei, MyWeb3
from test_wallet_distributor.test_wallet_distributor import TestWalletDistributor
from test_oracle_example.test_oracle_example import TestOracleExample
from clients.oracle_node_client import OracleNodeClient
from handler.config_handler import ConfigHandler


class TestOracleNodeClientDaemon(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._test_owner = ConfigHandler(_TEST_CONFIG).get_test_owner()
        try:
            MyDeployer(_TEST_CONFIG).undeploy()
        except IOError:
            pass
        # I don't deploy because node will help me deploy

    @classmethod
    def tearDownClass(cls):
        MyDeployer(_TEST_CONFIG).undeploy()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def reset_callback_event(self):
        self._callback_event.clear()

    def to_oracle_node_event_callback(self, node, event):
        self._callback_event.set()

    def run_node_client_daemon(self):
        oracle_node_client = OracleNodeClient(config_path=_TEST_CONFIG,
                                              to_oracle_node_callback_objs=[self],
                                              wait_time=1,
                                              deployed=True,
                                              deployed_event=self._deployed_event)
        oracle_node_client.start()
        oracle_node_client.join()

    def test_daemon_brandnew(self):
        self._callback_event = multiprocessing.Event()
        self._deployed_event = multiprocessing.Event()
        p = multiprocessing.Process(target=self.run_node_client_daemon)
        p.start()

        self._deployed_event.wait()

        myWeb3 = MyWeb3(_TEST_CONFIG)
        other_user = myWeb3.get_accounts()[3]
        payment_value = convert_to_wei(1000, 'wei')

        test_distributor = TestWalletDistributor(_TEST_CONFIG)
        now_balance = test_distributor.get_balance()

        eth_price = get_eth_price()
        test_distributor.deposit_balance(int(eth_price * 2), **{
            'value': payment_value,
            'from': other_user
        })
        new_balance = test_distributor.get_balance()
        self.assertEqual(new_balance, now_balance + payment_value, 'Should be the same')
        now_balance = new_balance

        test_example = TestOracleExample(_TEST_CONFIG)
        test_example.deposit(**{
            'value': convert_to_wei(20000, 'wei'),
            'from': self._test_owner
        })
        test_example.trigger(**{'from': self._test_owner})

        self._callback_event.wait()
        self.reset_callback_event()

        new_balance = test_distributor.get_balance()
        self.assertEqual(new_balance, now_balance, 'Should be the same')
        now_balance = new_balance

        eth_price = get_eth_price()
        test_distributor.deposit_balance(int(eth_price / 2), **{
            'value': payment_value,
            'from': other_user
        })
        new_balance = test_distributor.get_balance()
        self.assertEqual(new_balance, now_balance + payment_value, 'Should be the same')
        now_balance = new_balance
        test_example.deposit(**{
            'value': convert_to_wei(20000, 'wei'),
            'from': self._test_owner
        })
        test_example.trigger(**{'from': self._test_owner})

        self._callback_event.wait()
        self.reset_callback_event()

        new_balance = test_distributor.get_balance()
        self.assertEqual(new_balance, 0, 'Should be the same')

        p.terminate()
        p.join()


if __name__ == '__main__':
    unittest.main()
