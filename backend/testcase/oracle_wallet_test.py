#!/usr/bin/env python3
# encoding: utf-8

import unittest
import sys
sys.path.append('src')

from utils.my_deployer import MyDeployer
from test_utils import _TEST_CONFIG
from test_oracle_example.test_oracle_example import TestOracleExample
from utils.chain_utils import convert_to_wei, MyWeb3
from oracle_wallet.oracle_wallet import OracleWallet


class TestOracleWallet(unittest.TestCase):

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

    def test_single_event(self):
        myWeb3 = MyWeb3(_TEST_CONFIG)
        test_example = TestOracleExample(_TEST_CONFIG)
        PAYMENT_VALUE = 1000
        oracle_wallet = OracleWallet(_TEST_CONFIG)
        before_wallet_balance = oracle_wallet.get_balance()
        test_example.deposit(value=convert_to_wei(20000, 'wei'))
        test_example.trigger(value=convert_to_wei(PAYMENT_VALUE, 'wei'))
        after_wallet_balance = oracle_wallet.get_balance()

        self.assertEqual(before_wallet_balance + PAYMENT_VALUE,
                         after_wallet_balance,
                         'balance should be the same')

        accounts = myWeb3.get_accounts()
        before_wallet_balance = oracle_wallet.get_balance()
        before_account_balance = myWeb3.get_address_balance(accounts[1])
        oracle_wallet.withdraw(accounts[1])
        after_account_balance = myWeb3.get_address_balance(accounts[1])
        after_wallet_balance = oracle_wallet.get_balance()

        self.assertEqual(before_wallet_balance - PAYMENT_VALUE,
                         after_wallet_balance,
                         'balance should be the same')
        self.assertEqual(before_account_balance + before_wallet_balance,
                         after_account_balance,
                         'balance should be the same')


if __name__ == '__main__':
    unittest.main()
