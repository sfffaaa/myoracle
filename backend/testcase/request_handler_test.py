#!/usr/bin/env python3

import unittest
import sys
sys.path.append('src')

from handler.request_handler import RequestHandler


class TestRequestHandler(unittest.TestCase):

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

    def test_request_handler(self):
        request_handler = RequestHandler('json(https://api.kraken.com/0/public/Ticker?pair=ETHUSD)["result"]["XETHZUSD"]["c"][0]')
        self.assertEqual(request_handler._type, 'json')
        self.assertEqual(request_handler._request, 'https://api.kraken.com/0/public/Ticker?pair=ETHUSD')
        self.assertEqual(request_handler._parse_format, '["result"]["XETHZUSD"]["c"][0]')

    def test_fail_request_handler(self):
        request_handler = RequestHandler('json(https://api.kraken.com/0/public/Ticker)["error"][0]')
        self.assertEqual(request_handler._type, 'json')
        self.assertEqual(request_handler._request, 'https://api.kraken.com/0/public/Ticker')
        self.assertEqual(request_handler._parse_format, '["error"][0]')
        self.assertEqual(request_handler.execute_request(), 'EGeneral:Invalid arguments', 'should be the same')


if __name__ == '__main__':
    unittest.main()
