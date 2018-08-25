#!/usr/bin/env python3
# encoding: utf-8

from web3 import Web3
from utils import my_config
import time
from handler.contract_handler import ConfigHandler


def convert_to_wei(val, unit):
    return Web3.toWei(val, unit)


def convert_to_bytes(val):
    if bytes == type(val):
        return val
    elif val.startswith('0x'):
        return Web3.toBytes(hexstr=val)
    else:
        return Web3.toBytes(text=val)


def convert_to_hex(val):
    if str == type(val):
        return val
    return Web3.toHex(val)


def wait_miner(w3, tx_hashs):
    if type(tx_hashs) == list:
        test_tx_hashs = tx_hashs
    else:
        test_tx_hashs = [tx_hashs]

    tx_receipts = [w3.eth.getTransactionReceipt(_) for _ in test_tx_hashs]
    w3.miner.start(1)
    retry_time = 0
    while None in tx_receipts and retry_time < 15:
        print('    wait for miner {0} !'.format(retry_time))
        time.sleep(my_config.MINER_WAIT_TIME)
        tx_receipts = [w3.eth.getTransactionReceipt(_) for _ in test_tx_hashs]
        retry_time += 1

    if None in tx_receipts:
        raise IOError('miner not finished...'.format(tx_receipts))

    # w3.miner.stop()
    return tx_receipts


def check_transaction_meet_assert(w3, tx_hashs):
    if type(tx_hashs) == list:
        test_tx_hashs = tx_hashs
    else:
        test_tx_hashs = [tx_hashs]

    for tx_hash in test_tx_hashs:
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        if not tx_receipt:
            raise IOError('{0} receipt does not exist'.format(tx_hash))
        if tx_receipt.gasUsed == my_config.GAS_SPENT:
            return True

    return False


class MyWeb3():
    def __init__(self, config_path):
        self._w3 = self._get_web3_instance(config_path)

    def _get_web3_instance(self, config_path):
        config_handler = ConfigHandler(config_path)
        return config_handler.get_web3()

    def get_address_balance(self, address):
        return self._w3.eth.getBalance(address)

    def get_accounts(self):
        return self._w3.eth.accounts

    def get_tx_detail(self, tx):
        return self._w3.eth.getTransaction(tx)

    def get_tx_receipt(self, tx):
        return self._w3.eth.getTransactionReceipt(tx)
