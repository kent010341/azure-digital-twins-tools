import requests
import json
from .RequestHelper import RequestHelper

class PropertyHelper(RequestHelper):

    def __init__(self, token_path, host_name):
        super().__init__(token_path, host_name)
        self._is_preparing = False

    def get_twin_detail(self, dtid):
        method = requests.get
        uri = 'digitaltwins/{}'.format(dtid)

        return self.request(uri, method)

    def prepare(self, dtid):
        self._dtid = dtid
        self.update_process = list()
        self._is_preparing = True

        return self

    def update_property(self, key, value):
        assert self._is_preparing, \
            'The method \'update_property\' can\'t be used without using the method \'prepare\' before.'

        self.update_process.append(self._get_body('replace', key, value))

        return self

    def add_property(self, key, value):
        assert self._is_preparing, \
            'The method \'update_property\' can\'t be used without using the method \'prepare\' before.'

        self.update_process.append(self._get_body('add', key, value))

        return self

    def remove_property(self, key):
        assert self._is_preparing, \
            'The method \'update_property\' can\'t be used without using the method \'prepare\' before.'
            
        self.update_process.append(self._get_body('remove', key))
        
        return self

    def submit(self):
        method = requests.patch
        uri = 'digitaltwins/{}'.format(self._dtid)

        return self.request(uri, method, body=json.dumps(self.update_process))

    def _get_body(self, op, key, value=None):
        opt = {'op': op, 'path': '/' + key}
        
        if value != None:
            opt['value'] = value        

        return opt
