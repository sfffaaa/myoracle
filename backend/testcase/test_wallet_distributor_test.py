#!/usr/bin/env python3
# encoding: utf-8

import unittest
import sys
sys.path.append('src')

from utils.my_deployer import MyDeployer
from test_utils import _TEST_CONFIG
from utils.chain_utils import convert_to_wei, MyWeb3
from hodl_saver.hodl_saver import HodlSaver
from handler.config_handler import ConfigHandler


class TestHodlSaver(unittest.TestCase):

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
        other_user = myWeb3.get_accounts()[3]

        hodl_saver = HodlSaver(_TEST_CONFIG)
        all_events = hodl_saver.get_all_events()
        deposit_balance_event_hdr = all_events.DepositBalance.createFilter(fromBlock='latest')
        withdraw_balance_event_hdr = all_events.WithdrawBalance.createFilter(fromBlock='latest')
        PAYMENT_VALUE = 1000

        now_balance = hodl_saver.get_balance()
        hodl_saver.deposit_balance(100, **{
            'value': convert_to_wei(PAYMENT_VALUE, 'wei'),
            'from': other_user
        })
        deposit_balance_event = deposit_balance_event_hdr.get_new_entries()
        self.check_event_deposit_balance(other_user,
                                         100,
                                         convert_to_wei(PAYMENT_VALUE, 'wei'),
                                         now_balance + convert_to_wei(PAYMENT_VALUE, 'wei'),
                                         deposit_balance_event)
        now_balance = hodl_saver.get_balance()

        hodl_saver.deposit_balance(200, **{
            'value': convert_to_wei(50000, 'wei'),
            'from': other_user
        })
        deposit_balance_event = deposit_balance_event_hdr.get_new_entries()
        self.check_event_deposit_balance(other_user,
                                         200,
                                         convert_to_wei(50000, 'wei'),
                                         now_balance + convert_to_wei(50000, 'wei'),
                                         deposit_balance_event)
        now_balance = hodl_saver.get_balance()

        hodl_saver.withdraw_balance(199, **{
            'from': self._test_owner
        })
        withdraw_balance_event = withdraw_balance_event_hdr.get_new_entries()
        self.check_event_withdraw_balance(other_user,
                                          200,
                                          199,
                                          False,
                                          withdraw_balance_event)
        self.assertEqual(now_balance,
                         hodl_saver.get_balance(),
                         'balance should be the same')

        hodl_saver.withdraw_balance(201, **{
            'from': self._test_owner
        })
        withdraw_balance_event = withdraw_balance_event_hdr.get_new_entries()
        self.check_event_withdraw_balance(other_user,
                                          200,
                                          201,
                                          True,
                                          withdraw_balance_event)
        self.assertEqual(0,
                         hodl_saver.get_balance(),
                         'balance should be the same')


if __name__ == '__main__':
    unittest.main()
