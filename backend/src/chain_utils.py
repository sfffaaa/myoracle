#!/usr/bin/env python3
# encoding: utf-8

from web3 import Web3
import my_config
import time


def calculate_entry_hash(input_vals):
    hash_sums = [Web3.toInt(Web3.sha3(text=str(val))) for val in input_vals]
    return Web3.toHex(Web3.sha3(sum(hash_sums) & (2 ** 256 - 1)))


def convert_to_bytes(val):
    if bytes == type(val):
        return val
    elif val.startswith('0x'):
        return Web3.toBytes(hexstr=val)
    else:
        return Web3.toBytes(text=val)


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
