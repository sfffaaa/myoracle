#!/usr/bin/env python3
# encoding: utf-8

import os
import zmq
from utils.my_config import FEE_IPC_FILE, FEE_IPC_URL


class FeeCollectServer():

    def __init__(self):
        context = zmq.Context()
        self._server_socket = context.socket(zmq.REP)
        self._server_socket.bind(FEE_IPC_URL)
        self._attach_data = []

    def _command_dispatcher(self, raw_data):
        if 'command' not in raw_data:
            print('skip data {0}'.format(raw_data))
            self._server_socket.send_string('')
        elif 'attach' == raw_data['command']:
            self._attach_data.append(raw_data['data'])
            self._server_socket.send_string('')
        elif 'get' == raw_data['command']:
            # return attach data
            self._server_socket.send_json(self._attach_data)
        elif 'reset' == raw_data['command']:
            self._attach_data = []
            self._server_socket.send_string('')
        elif 'stop' == raw_data['command']:
            self._run = False
            self._server_socket.send_string('')

    def run(self):
        self._run = True
        while self._run:
            raw_data = self._server_socket.recv_json()
            self._command_dispatcher(raw_data)
        print('wwww???')
        print(os.path.isfile(FEE_IPC_FILE))
        os.unlink(FEE_IPC_FILE)
        print(os.path.isfile(FEE_IPC_FILE))
        print('@@@')


if __name__ == '__main__':
    server = FeeCollectServer()
    server.run()
