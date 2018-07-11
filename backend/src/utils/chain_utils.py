#!/usr/bin/env python3
# encoding: utf-8

from web3 import Web3
from utils import my_config
import time


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
    while None in tx_receipts and retry_time < 10:
        print('    wait for miner!')
        time.sleep(my_config.MINER_WAIT_TIME)
        tx_receipts = [w3.eth.getTransactionReceipt(_) for _ in test_tx_hashs]
        retry_time += 1

    w3.miner.stop()
    return tx_receipts


def check_transaction_meet_assert(w3, tx_hashs):
    if type(tx_hashs) == list:
        test_tx_hashs = tx_hashs
    else:
        test_tx_hashs = [tx_hashs]

    for tx_hash in test_tx_hashs:
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        if not tx_receipt:
            raise IOError('{0} receipt does not exist'.format(tx_receipt))
        if tx_receipt.gasUsed == my_config.GAS_SPENT:
            return True

    return False
