import requests
import json

_TEST_CONFIG = 'testcase/etc/test_config.conf'


def get_eth_price():
    r = requests.get('https://api.kraken.com/0/public/Ticker?pair=ETHUSD')
    return float(json.loads(r.text)["result"]["XETHZUSD"]["c"][0])
