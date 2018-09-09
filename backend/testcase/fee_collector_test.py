#!/usr/bin/env python3
# encoding: utf-8

import unittest
import sys
sys.path.append('src')

from utils.fee_collector_utils import start_fee_server_in_new_process
from fee_collector.fee_collector_client import FeeCollectClient


class TestFeeCollector(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @start_fee_server_in_new_process
    def test_collector(self):
        CHECK_DATA = [{'money': 'show me the money'}, {'serious': 'why so serious'}]
        fee_collector_client = FeeCollectClient()
        fee_collector_client.attach(CHECK_DATA[0])
        fee_collector_client.attach(CHECK_DATA[1])
        data = fee_collector_client.get()
        self.assertEqual(CHECK_DATA, data, 'should be the same')


if __name__ == '__main__':
    unittest.main()
