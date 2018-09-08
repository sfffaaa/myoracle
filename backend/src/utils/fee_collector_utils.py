#!/usr/bin/env python3
# encoding: utf-8

import os
from fee_collector.fee_collector_server import FeeCollectServer
from utils.my_config import FEE_IPC_FILE
import multiprocessing


def start_fee_server_in_new_process(f):
    def start_server():
        fee_collector_server = FeeCollectServer()
        fee_collector_server.run()

    def my_wrapper(*args, **kargs):
        p = multiprocessing.Process(target=start_server)
        p.start()
        ret = f(*args, **kargs)
        p.terminate()
        p.join()
        os.unlink(FEE_IPC_FILE)
        return ret

    return my_wrapper
