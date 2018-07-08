#!/usr/bin/env python3
# encoding: utf-8

import gevent
import my_config

SETUP_EVENT_KEYS = ['contract_name', 'event_name', 'callback_objs', 'event_filter', 'contract_handler',
                    'callback_name']


class BaseChainNode(gevent.Greenlet):

    def __init__(self,
                 config_path=my_config.CONFIG_PATH,
                 wait_time=3):
        super(BaseChainNode, self).__init__()
        self.wait_time = wait_time
        self._setup_event_emitter(config_path)

    def setup_event(self, contract_inst):
        IOError('You should implement in your child')

    def setup_contract(self, contract):
        IOError('You should implement in your child')

    def _setup_one_event_emitter(self, setting):
        if not all(k in setting.keys() for k in SETUP_EVENT_KEYS):
            raise IOError('{0} doesn\'t have {1}'.format(setting.keys(), SETUP_EVENT_KEYS))

        for k, v in setting.items:
            if k in ['contract_name', 'event_name']:
                continue
            self._event_emitter[setting['contract_name']][setting['event_name']][k] = v
        '''
            setting: {
                'contract_name': {
                    'event_name': {
                        'contract_handler': contract_handler,
                        'callback_objs': callbacks
                        'event_filter': filter
                    }
                }
            }
        '''

    def _setup_event_emitter(self, config_path):
        self._event_emitter = {}
        for setting in self.setup_contract(config_path):
            self._setup_one_event_emitter(setting)

    def _run(self):
        while True:
            for _, contract_entry in self._event_emitter.items():
                for event_name, event_entry in contract_entry.items():
                    for event in event_entry['event_filter'].get_new_entries():
                        for callback_obj in event_entry['callback_objs']:
                            callback_func = getattr(callback_obj, event_entry['callback_name'])
                            callback_func(self, event)

            gevent.sleep(self.wait_time)


if __name__ == '__main__':
    base_chain_node = BaseChainNode()
    base_chain_node.start()
    base_chain_node.join()
