#!/usr/bin/env python3

import gevent
import unittest
import sys
sys.path.append('src')

from utils.my_deployer import MyDeployer
from clients.oracle_node_client import OracleNodeClient
from test_utils import _TEST_CONFIG, get_eth_price
from utils.chain_utils import convert_to_wei, MyWeb3
from hodl_saver.hodl_saver import HodlSaver
from hodl_oracle.hodl_oracle import HodlOracle
from oracle_fee_wallet.oracle_fee_wallet import OracleFeeWallet
from handler.config_handler import ConfigHandler
from utils.fee_collector_utils import start_fee_server_in_new_process, get_all_fee_reports


class TestBehavior(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._hodl_owner = ConfigHandler(_TEST_CONFIG).get_hodl_owner()
        MyDeployer(_TEST_CONFIG).deploy()

    @classmethod
    def tearDownClass(cls):
        MyDeployer(_TEST_CONFIG).undeploy()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @start_fee_server_in_new_process
    def test_behavior(self):
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

        node_daemon = OracleNodeClient(config_path=_TEST_CONFIG,
                                       wait_time=1)
        node_daemon.start()

        test_example = HodlOracle(_TEST_CONFIG)
        test_example.deposit(**{
            'value': convert_to_wei(20000, 'wei'),
            'from': self._hodl_owner
        })
        oracle_fee_wallet = OracleFeeWallet(_TEST_CONFIG)
        self.assertEqual(oracle_fee_wallet.get_balance(test_example.get_address()),
                         convert_to_wei(20000, 'wei'),
                         'should be the same in balance')
        test_example.trigger(**{
            'from': self._hodl_owner
        })

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
        test_example.deposit(**{
            'value': convert_to_wei(20000, 'wei'),
            'from': self._hodl_owner
        })
        test_example.trigger(**{
            'from': self._hodl_owner
        })

        for _ in range(15):
            gevent.sleep(2)
            new_balance = hodl_saver.get_balance()
            if new_balance != now_balance:
                break

        new_balance = hodl_saver.get_balance()
        self.assertEqual(new_balance, 0, 'Should be the same')

        node_daemon.kill()
        self.assertEqual(oracle_fee_wallet.get_balance(test_example.get_address()),
                         convert_to_wei(0, 'wei'),
                         'should be the same in balance')
        get_all_fee_reports()


if __name__ == '__main__':
    unittest.main()
