#!/usr/bin/env python3
# encoding: utf-8

import unittest
import sys
sys.path.append('src')

from utils.my_deployer import MyDeployer
from test_utils import _TEST_CONFIG
from utils.chain_utils import convert_to_wei, MyWeb3
from test_wallet_distributor.test_wallet_distributor import TestWalletDistributor


class TestTestWalletDistributor(unittest.TestCase):

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

    def check_event_deposit_balance(self, address, threshold, now_value, accu_value, events):
        self.assertEqual(len(events),
                         1,
                         'should have one event here')
        event = events[0]['args']
        self.assertEqual(address, event.myAddress, 'account should be the same')
        self.assertEqual(threshold, event.threshold, 'threshold should be the same')
        self.assertEqual(now_value, event.nowValue, 'now value shold be the same')
        self.assertEqual(accu_value, event.accuValue, 'accumulate value should be the same')

    def check_event_withdraw_balance(self, address, threshold, price, transfered, events):
        self.assertEqual(len(events),
                         1,
                         'should have one event here')
        event = events[0]['args']
        self.assertEqual(address, event.myAddress, 'account should be the same')
        self.assertEqual(threshold, event.threshold, 'threshold should be the same')
        self.assertEqual(price, event.price, 'price shold be the same')
        self.assertEqual(transfered, event.transfered, 'transfered should be the same')

    def test_basic_test(self):
        myWeb3 = MyWeb3(_TEST_CONFIG)
        accounts = myWeb3.get_accounts()

        test_distributor = TestWalletDistributor(_TEST_CONFIG)
        all_events = test_distributor.get_all_events()
        deposit_balance_event_hdr = all_events.DepositBalance.createFilter(fromBlock='latest')
        withdraw_balance_event_hdr = all_events.WithdrawBalance.createFilter(fromBlock='latest')
        PAYMENT_VALUE = 1000

        now_balance = test_distributor.get_balance()
        test_distributor.deposit_balance(100, **{
            'value': convert_to_wei(PAYMENT_VALUE, 'wei'),
            'from': accounts[0]
        })
        deposit_balance_event = deposit_balance_event_hdr.get_new_entries()
        self.check_event_deposit_balance(accounts[0],
                                         100,
                                         convert_to_wei(PAYMENT_VALUE, 'wei'),
                                         now_balance + convert_to_wei(PAYMENT_VALUE, 'wei'),
                                         deposit_balance_event)
        now_balance = test_distributor.get_balance()

        test_distributor.deposit_balance(200, **{
            'value': convert_to_wei(50000, 'wei'),
            'from': accounts[0]
        })
        deposit_balance_event = deposit_balance_event_hdr.get_new_entries()
        self.check_event_deposit_balance(accounts[0],
                                         200,
                                         convert_to_wei(50000, 'wei'),
                                         now_balance + convert_to_wei(50000, 'wei'),
                                         deposit_balance_event)
        now_balance = test_distributor.get_balance()

        test_distributor.withdraw_balance(199)
        withdraw_balance_event = withdraw_balance_event_hdr.get_new_entries()
        self.check_event_withdraw_balance(accounts[0],
                                          200,
                                          199,
                                          False,
                                          withdraw_balance_event)
        self.assertEqual(now_balance,
                         test_distributor.get_balance(),
                         'balance should be the same')

        test_distributor.withdraw_balance(201)
        withdraw_balance_event = withdraw_balance_event_hdr.get_new_entries()
        self.check_event_withdraw_balance(accounts[0],
                                          200,
                                          201,
                                          True,
                                          withdraw_balance_event)
        self.assertEqual(0,
                         test_distributor.get_balance(),
                         'balance should be the same')


if __name__ == '__main__':
    unittest.main()
