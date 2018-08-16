#!/usr/bin/env python3
# encoding: utf-8

import gevent
import unittest
import sys
sys.path.append('src')

from utils.my_deployer import MyDeployer
from test_utils import _TEST_CONFIG, get_eth_price
from utils.chain_utils import convert_to_wei, MyWeb3
from test_wallet_distributor.test_wallet_distributor import TestWalletDistributor
from test_oracle_example.test_oracle_example import TestOracleExample
import time
import os


class TestOracleNodeClientDaemon(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            MyDeployer(_TEST_CONFIG).undeploy()
        except IOError:
            pass
        else:
            raise

    @classmethod
    def tearDownClass(cls):
        MyDeployer(_TEST_CONFIG).undeploy()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def run_node_client_daemon(self):
        os.system('python3 bin/oracle_node_client_daemon.py -c {0} -d &'.format(_TEST_CONFIG))
        time.sleep(120)

    def test_daemon_brandnew(self):
        self.run_node_client_daemon()

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

        for _ in range(15):
            gevent.sleep(2)
            new_balance = test_distributor.get_balance()
            if new_balance != now_balance:
                break

        new_balance = test_distributor.get_balance()
        self.assertEqual(new_balance, 0, 'Should be the same')


if __name__ == '__main__':
    unittest.main()
