#!/usr/bin/env python3
# encoding: utf-8

import unittest
import sys
sys.path.append('src')

from utils.my_deployer import MyDeployer
from test_utils import _TEST_CONFIG
from utils.chain_utils import convert_to_wei, MyWeb3
from oracle_fee_wallet.oracle_fee_wallet import OracleFeeWallet
from utils.fee_collector_utils import start_fee_server_in_new_process, get_all_fee_reports


class TestOracleFeeWallet(unittest.TestCase):

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

    def _check_deposit_action_event(self, events, check_dict):
        self.assertEqual(len(events),
                         1,
                         'should have one event here')

        event = events[0]['args']
        self.assertEqual(check_dict['address'],
                         event.sender,
                         'account should be the same')

        self.assertEqual(check_dict['sent_value'],
                         event.value,
                         'now value shold be the same')

        self.assertEqual(check_dict['accumulate_value'],
                         event.accumulateValue,
                         'accumulate value should be the same')

    def check_deposit(self, oracle_fee_wallet, deposit_action_event_hdr, check_dict):
        oracle_fee_wallet.deposit(**{
            'from': check_dict['address'],
            'value': check_dict['sent_value']
        })
        deposit_action_events = deposit_action_event_hdr.get_new_entries()
        self._check_deposit_action_event(deposit_action_events, check_dict)

    @start_fee_server_in_new_process
    def test_single_event(self):
        myWeb3 = MyWeb3(_TEST_CONFIG)
        accounts = myWeb3.get_accounts()
        oracle_fee_wallet = OracleFeeWallet(_TEST_CONFIG)

        all_events = oracle_fee_wallet.get_all_events()
        deposit_action_event_hdr = all_events.DepositAction.createFilter(fromBlock='latest')

        self.check_deposit(oracle_fee_wallet, deposit_action_event_hdr, {
            'address': accounts[1],
            'sent_value': convert_to_wei(5000, 'wei'),
            'accumulate_value': convert_to_wei(5000, 'wei')
        })

        self.check_deposit(oracle_fee_wallet, deposit_action_event_hdr, {
            'address': accounts[2],
            'sent_value': convert_to_wei(10000, 'wei'),
            'accumulate_value': convert_to_wei(10000, 'wei')
        })

        self.check_deposit(oracle_fee_wallet, deposit_action_event_hdr, {
            'address': accounts[1],
            'sent_value': convert_to_wei(7000, 'wei'),
            'accumulate_value': convert_to_wei(12000, 'wei')
        })
        get_all_fee_reports()


if __name__ == '__main__':
    unittest.main()
