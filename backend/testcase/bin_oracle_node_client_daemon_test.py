#!/usr/bin/env python3
# encoding: utf-8

import unittest
import sys
import multiprocessing
sys.path.append('src')

from utils.my_deployer import MyDeployer
from test_utils import _TEST_CONFIG, get_eth_price
from utils.chain_utils import convert_to_wei, MyWeb3
from hodl_saver.hodl_saver import HodlSaver
from hodl_oracle.hodl_oracle import HodlOracle
from clients.oracle_node_client import OracleNodeClient
from handler.config_handler import ConfigHandler
from utils.fee_collector_utils import start_fee_server_in_new_process, get_all_fee_reports


class TestOracleNodeClientDaemon(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._hodl_owner = ConfigHandler(_TEST_CONFIG).get_hodl_owner()
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

    @start_fee_server_in_new_process
    def test_daemon_brandnew(self):
        self._callback_event = multiprocessing.Event()
        self._deployed_event = multiprocessing.Event()
        p = multiprocessing.Process(target=self.run_node_client_daemon)
        p.start()

        self._deployed_event.wait()

        myWeb3 = MyWeb3(_TEST_CONFIG)
        other_user = myWeb3.get_accounts()[3]
        payment_value = convert_to_wei(1000, 'wei')

        hodl_saver = HodlSaver(_TEST_CONFIG)
        now_balance = hodl_saver.get_balance()

        eth_price = get_eth_price()
        hodl_saver.deposit_balance(int(eth_price * 2), **{
            'value': payment_value,
            'from': other_user
        })
        new_balance = hodl_saver.get_balance()
        self.assertEqual(new_balance, now_balance + payment_value, 'Should be the same')
        now_balance = new_balance

        hodl_oracle = HodlOracle(_TEST_CONFIG)
        hodl_oracle.deposit(**{
            'value': convert_to_wei(20000, 'wei'),
            'from': self._hodl_owner
        })
        hodl_oracle.trigger(**{'from': self._hodl_owner})

        self._callback_event.wait()
        self.reset_callback_event()

        new_balance = hodl_saver.get_balance()
        self.assertEqual(new_balance, now_balance, 'Should be the same')
        now_balance = new_balance

        eth_price = get_eth_price()
        hodl_saver.deposit_balance(int(eth_price / 2), **{
            'value': payment_value,
            'from': other_user
        })
        new_balance = hodl_saver.get_balance()
        self.assertEqual(new_balance, now_balance + payment_value, 'Should be the same')
        now_balance = new_balance
        hodl_oracle.deposit(**{
            'value': convert_to_wei(20000, 'wei'),
            'from': self._hodl_owner
        })
        hodl_oracle.trigger(**{'from': self._hodl_owner})

        self._callback_event.wait()
        self.reset_callback_event()

        new_balance = hodl_saver.get_balance()
        self.assertEqual(new_balance, 0, 'Should be the same')

        p.terminate()
        p.join()
        get_all_fee_reports()


if __name__ == '__main__':
    unittest.main()
