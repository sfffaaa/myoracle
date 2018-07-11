#!/usr/bin/env python3
# encoding: utf-8

import my_config


class BaseContract():

    def __init__(self, config=my_config.CONFIG_PATH):
        self._onchain_handler = self.create_onchain_handler(config)

    def create_onchain_handler(self, config):
        raise IOError('Child should implement this function')

    def get_all_events(self):
        return self._onchain_handler.get_all_events()
