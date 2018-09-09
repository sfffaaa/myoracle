#!/usr/bin/env python3
# encoding: utf-8

import unittest
import sys
sys.path.append('src')

from utils.my_deployer import MyDeployer
from test_utils import _TEST_CONFIG
from hodl_oracle.hodl_oracle import HodlOracle
from utils.chain_utils import convert_to_wei, MyWeb3
from oracle_wallet.oracle_wallet import OracleWallet
from oracle_fee_wallet.oracle_fee_wallet import OracleFeeWallet
from handler.config_handler import ConfigHandler
from utils.fee_collector_utils import start_fee_server_in_new_process, get_all_fee_reports


class TestOracleWallet(unittest.TestCase):

    @classmethod
    @start_fee_server_in_new_process
    def setUpClass(cls):
        cls._hodl_owner = ConfigHandler(_TEST_CONFIG).get_hodl_owner()
        cls._oracle_owner = ConfigHandler(_TEST_CONFIG).get_oracle_owner()
        MyDeployer(_TEST_CONFIG).deploy()
        get_all_fee_reports()

    @classmethod
    def tearDownClass(cls):
        MyDeployer(_TEST_CONFIG).undeploy()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @start_fee_server_in_new_process
    def test_single_event(self):
        myWeb3 = MyWeb3(_TEST_CONFIG)
        hodl_oracle = HodlOracle(_TEST_CONFIG)
        PAYMENT_VALUE = 10000
        oracle_wallet = OracleWallet(_TEST_CONFIG)
        before_wallet_balance = oracle_wallet.get_balance()
        hodl_oracle.deposit(**{
            'value': convert_to_wei(PAYMENT_VALUE, 'wei'),
            'from': self._hodl_owner
        })
        hodl_oracle.trigger(**{
            'from': self._hodl_owner
        })

        oracle_fee_wallet = OracleFeeWallet(_TEST_CONFIG)
        oracle_fee_wallet.payback(**{
            'from': self._oracle_owner
        })

        after_wallet_balance = oracle_wallet.get_balance()
        self.assertEqual(before_wallet_balance + convert_to_wei(PAYMENT_VALUE, 'wei'),
                         after_wallet_balance,
                         'balance should be the same')

        other_user = myWeb3.get_accounts()[3]
        before_wallet_balance = oracle_wallet.get_balance()
        before_account_balance = myWeb3.get_address_balance(other_user)
        oracle_wallet.withdraw(other_user, **{
            'from': self._oracle_owner
        })
        after_account_balance = myWeb3.get_address_balance(other_user)
        after_wallet_balance = oracle_wallet.get_balance()

        self.assertEqual(before_wallet_balance - PAYMENT_VALUE,
                         after_wallet_balance,
                         'balance should be the same')
        self.assertEqual(before_account_balance + before_wallet_balance,
                         after_account_balance,
                         'balance should be the same')
        get_all_fee_reports()


if __name__ == '__main__':
    unittest.main()
