#!/usr/bin/env python3
# encoding: utf-8


import configparser
from utils.my_config import CONFIG_PATH


class ConfigHandler():
    def __init__(self, config_path=CONFIG_PATH):
        self._config_path = config_path

    def get_chain_config(self, section, key):
        config = configparser.ConfigParser()
        config.read(self._config_path)
        return config.get(section, key)
