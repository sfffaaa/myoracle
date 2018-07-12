#!/usr/bin/env python3
# encoding: utf-8

import re
import requests
import json

NOW_DEFINED_TYPE = ['json']


class RequestHandler():
    def __init__(self, request_data):
        self._request_data = request_data
        if request_data.startswith('json('):
            self._type = 'json'
            self._process_json_request_data(request_data)
        else:
            raise IOError('Doesn\'t find {0} type'.format(request_data))

    def _process_json_request_data(self, request_data):
        if not re.match(r'^json\((.*?)\)((?:\[.*?\])+)$', request_data):
            raise IOError('data {0} have more or less than 1 "("'.format(request_data))

        req = re.search(r'^json\((.*?)\)((?:\[.*?\])+)$', request_data).groups()
        self._request, self._parse_format = req

    def _parse_json_type(self, text):
        data = json.loads(text)
        for key in re.findall(r'\[(.*?)\]', self._parse_format):
            if re.match(r'([\'"]).*?\1', key):
                key = re.search(r'([\'"])(.*?)\1', key).group(2)
                data = data[key]
            elif re.match(r'^\d+$', key):
                data = data[int(key)]
            else:
                raise IOError('{0} is strange...'.format(key))
        return data

    def execute_request(self):
        r = requests.get(self._request)
        if self._type == 'json':
            return self._parse_json_type(r.text)
        else:
            raise IOError('Not implemnt {0}'.format(self._type))
