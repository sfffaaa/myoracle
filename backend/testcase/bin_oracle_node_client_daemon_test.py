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
import time


def run_node_client_daemon():
    oracle_node_client = OracleNodeClient(config_path=_TEST_CONFIG,
                                          wait_time=1,
                                          deployed=True)
    oracle_node_client.start()
    oracle_node_client.join()


class TestOracleNodeClientDaemon(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
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

    def test_daemon_brandnew(self):
        p = multiprocessing.Process(target=run_node_client_daemon)
        p.start()

        for i in range(15):
            time.sleep(15)
            print('wait {0} seconds'.format(15 * i))

        myWeb3 = MyWeb3(_TEST_CONFIG)
        accounts = myWeb3.get_accounts()
        payment_value = convert_to_wei(1000, 'wei')

        test_distributor = TestWalletDistributor(_TEST_CONFIG)
        now_balance = test_distributor.get_balance()

        eth_price = get_eth_price()
        test_distributor.deposit_balance(int(eth_price * 2), **{
            'value': payment_value,
            'from': accounts[0]
        })
        new_balance = test_distributor.get_balance()
        self.assertEqual(new_balance, now_balance + payment_value, 'Should be the same')
        now_balance = new_balance

        test_example = TestOracleExample(_TEST_CONFIG)
        test_example.trigger(value=convert_to_wei(1000, 'wei'))

        for i in range(20):
            time.sleep(2)
            print('wait {0} seconds'.format(2 * i))

        new_balance = test_distributor.get_balance()
        self.assertEqual(new_balance, now_balance, 'Should be the same')
        now_balance = new_balance

        eth_price = get_eth_price()
        test_distributor.deposit_balance(int(eth_price / 2), **{
            'value': payment_value,
            'from': accounts[0]
        })
        new_balance = test_distributor.get_balance()
        self.assertEqual(new_balance, now_balance + payment_value, 'Should be the same')
        now_balance = new_balance
        test_example.trigger(value=convert_to_wei(1000, 'wei'))

        for i in range(30):
            time.sleep(2)
            print('wait {0} seconds'.format(2 * i))
            new_balance = test_distributor.get_balance()
            if new_balance != now_balance:
                break

        new_balance = test_distributor.get_balance()
        self.assertEqual(new_balance, 0, 'Should be the same')
        # wait for callback finish
        for i in range(10):
            time.sleep(2)
            print('wait {0} seconds'.format(2 * i))

        p.terminate()
        p.join()


if __name__ == '__main__':
    unittest.main()
