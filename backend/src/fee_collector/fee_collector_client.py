#!/usr/bin/env python3
# encoding: utf-8

import os
import zmq
from utils.my_config import FEE_IPC_URL, FEE_IPC_FILE


class FeeCollectClient():
    def __init__(self):
        if self.is_connected():
            self.connect()

    def is_connected(self):
        return os.path.exists(FEE_IPC_FILE)

    def connect(self):
        context = zmq.Context()
        self._client_socket = context.socket(zmq.REQ)
        self._client_socket.connect(FEE_IPC_URL)

    def stop(self):
        if not self.is_connected():
            return

        self._client_socket.send_json({
            'command': 'stop'
        })
        self._client_socket.recv_string()

    def gas_attach(self, name, function, fee):
        data = {
            'name': name,
            'func': function,
            'fee': fee
        }
        self.attach(data)

    def attach(self, data):
        if not self.is_connected():
            return

        self._client_socket.send_json({
            'command': 'attach',
            'data': data
        })
        self._client_socket.recv_string()

    def get(self):
        if not self.is_connected():
            return None

        self._client_socket.send_json({
            'command': 'get'
        })
        return self._client_socket.recv_json()


if __name__ == '__main__':
    client = FeeCollectClient()
    client.attach({'asdf': 'aa'})
    print(client.get())
