#!/usr/bin/env python3
# encoding: utf-8

import os
from fee_collector.fee_collector_server import FeeCollectServer
from fee_collector.fee_collector_client import FeeCollectClient
from utils.my_config import FEE_IPC_FILE
import multiprocessing


def start_fee_server_in_new_process(f):
    def start_server(start_event):
        fee_collector_server = FeeCollectServer()
        start_event.set()
        fee_collector_server.run()

    def my_wrapper(*args, **kargs):
        start_event = multiprocessing.Event()
        p = multiprocessing.Process(target=start_server, args=(start_event,))
        p.start()
        start_event.wait()
        ret = f(*args, **kargs)
        p.terminate()
        p.join()
        os.unlink(FEE_IPC_FILE)
        return ret

    return my_wrapper


def record_fee_client(obj_name, func_name, f):
    def my_wrapper(*args, **kargs):
        client = FeeCollectClient()
        ret = f(*args, **kargs)
        tx_receipts = ret
        if type(ret) != list:
            tx_receipts = [ret]
        if client.is_connected():
            for tx_receipt in tx_receipts:
                client.gas_attach(obj_name, func_name, tx_receipt['gasUsed'])
        return ret
    return my_wrapper


def get_all_fee_reports():
    client = FeeCollectClient()
    records = client.get()
    if not records:
        print('No reports, because server doesn\'t execute')
        return
    report_dict = {}
    for entry in records:
        key = '{0}_{1}'.format(entry['name'], entry['func'])
        count = 1 if key not in report_dict else report_dict[key]['count'] + 1
        fee = entry['fee'] if key not in report_dict else report_dict[key]['fee'] + entry['fee']
        report_dict[key] = {
            'name': entry['name'],
            'func': entry['func'],
            'fee': fee,
            'count': count
        }
    for v in report_dict.values():
        v['avg_fee'] = v['fee'] / float(v['count'])
    reports = [v for v in report_dict.values()]
    reports = sorted(reports, key=lambda x: x['fee'], reverse=True)
    print('======== start fee report ======== ')
    print('name func fee count avg_fee')
    for entry in reports:
        print('{0} {1} {2} {3} {4}'.format(entry['name'], entry['func'],
                                           entry['fee'], entry['count'],
                                           entry['avg_fee']))
    print('======== end fee report ========')


def record_gas_from_tx_receipts(data):
    client = FeeCollectClient()
    if client.is_connected():
        for entry in data:
            client.gas_attach(entry['name'], entry['func'], entry['txReceipt']['gasUsed'])
