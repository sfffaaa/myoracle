#!/usr/bin/env python3
# encoding: utf-8

import functools
from web3 import Web3
from handler.contract_handler import ConfigHandler


def contract_function_log(func):
    @functools.wraps(func)
    def func_wrapper(*args, **kargs):
        func_name = func.__name__[:]
        if func_name.startswith('c_'):
            func_name = func_name[2:]
        print('==== {0} start ===='.format(func_name))
        ret = func(*args, **kargs)
        print('==== {0} end ===='.format(func_name))
        return ret
    return func_wrapper


def convert_to_wei(val, unit):
    return Web3.toWei(val, unit)


def convert_to_bytes(val):
    if bytes == type(val):
        return val

    if val.startswith('0x'):
        return Web3.toBytes(hexstr=val)

    return Web3.toBytes(text=val)


def convert_to_hex(val):
    if str == type(val):
        return val
    return Web3.toHex(val)


def wait_miner(w3, tx_hashs):
    if isinstance(tx_hashs, list):
        test_tx_hashs = tx_hashs
    else:
        test_tx_hashs = [tx_hashs]

    w3.miner.start(1)
    tx_receipts = [w3.eth.waitForTransactionReceipt(_, timeout=240) for _ in test_tx_hashs]

    if None in tx_receipts:
        raise IOError('miner not finished... {0}'.format(tx_receipts))

    # w3.miner.stop()
    return tx_receipts


def check_tx_receipts_meet_assert(tx_receipts):
    if isinstance(tx_receipts, list):
        test_tx_receipts = tx_receipts
    else:
        test_tx_receipts = [tx_receipts]

    for tx_receipt in test_tx_receipts:
        if tx_receipt.status != 1:
            print('tx erceipt has error {0}'.format(tx_receipt))
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
