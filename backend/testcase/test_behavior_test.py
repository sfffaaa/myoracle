#!/usr/bin/env python3
# encoding: utf-8

import gevent
import unittest
import sys
sys.path.append('src')

from utils.my_deployer import MyDeployer
from clients.oracle_node_client import OracleNodeClient
from test_utils import _TEST_CONFIG, get_eth_price
from utils.chain_utils import convert_to_wei, MyWeb3
from test_wallet_distributor.test_wallet_distributor import TestWalletDistributor
from test_oracle_example.test_oracle_example import TestOracleExample
from oracle_fee_wallet.oracle_fee_wallet import OracleFeeWallet
from handler.config_handler import ConfigHandler


class TestBehavior(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._test_owner = ConfigHandler(_TEST_CONFIG).get_test_owner()
        MyDeployer(_TEST_CONFIG).deploy()

    @classmethod
    def tearDownClass(cls):
        MyDeployer(_TEST_CONFIG).undeploy()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_behavior(self):
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

        node_daemon = OracleNodeClient(config_path=_TEST_CONFIG,
                                       wait_time=1)
        node_daemon.start()

        test_example = TestOracleExample(_TEST_CONFIG)
        test_example.deposit(**{
            'value': convert_to_wei(20000, 'wei'),
            'from': self._test_owner
        })
        oracle_fee_wallet = OracleFeeWallet(_TEST_CONFIG)
        self.assertEqual(oracle_fee_wallet.get_balance(test_example.get_address()),
                         convert_to_wei(20000, 'wei'),
                         'should be the same in balance')
        test_example.trigger(**{
            'from': self._test_owner
        })

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
        test_example.trigger(**{
            'from': self._test_owner
        })

        for _ in range(15):
            gevent.sleep(2)
            new_balance = test_distributor.get_balance()
            if new_balance != now_balance:
                break

        new_balance = test_distributor.get_balance()
        self.assertEqual(new_balance, 0, 'Should be the same')

        node_daemon.kill()
        self.assertEqual(oracle_fee_wallet.get_balance(test_example.get_address()),
                         convert_to_wei(0, 'wei'),
                         'should be the same in balance')


if __name__ == '__main__':
    unittest.main()
