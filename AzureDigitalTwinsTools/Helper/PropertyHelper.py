import requests
import json
from .RequestHelper import RequestHelper

class PropertyHelper(RequestHelper):

    def __init__(self, token_path, host_name):
        super().__init__(token_path, host_name)
        self._is_preparing_p = False
        self._is_preparing_c = False

    def get_twin_detail(self, dtid):
        method = requests.get
        uri = 'digitaltwins/{}'.format(dtid)

        return self.request(uri, method)

    def prepare_property(self, dtid):
        assert not self._is_preparing_c, \
            'The process has already start for updating component.'

        self._dtid = dtid
        self.update_process = list()
        self._is_preparing_p = True

        return self

    def prepare_component(self, dtid, component_path):
        assert not self._is_preparing_p, \
            'The process has already start for updating property.'

        self._dtid = dtid
        self._component_path = component_path
        self.update_process = list()
        self._is_preparing_c = True

        return self

    def update_property(self, key, value):
        assert self._is_preparing_p or self._is_preparing_c, \
            'The method \'update_property\' can\'t be used without using the method \'prepare\' before.'

        self.update_process.append(self._get_body('replace', key, value))

        return self

    def add_property(self, key, value):
        assert self._is_preparing_p or self._is_preparing_c, \
            'The method \'update_property\' can\'t be used without using the method \'prepare\' before.'

        self.update_process.append(self._get_body('add', key, value))

        return self

    def remove_property(self, key):
        assert self._is_preparing_p or self._is_preparing_c, \
            'The method \'update_property\' can\'t be used without using the method \'prepare\' before.'
            
        self.update_process.append(self._get_body('remove', key))
        
        return self

    def submit(self):
        method = requests.patch
        if self._is_preparing_p:
            uri = 'digitaltwins/{}'.format(self._dtid)
        elif self._is_preparing_c:
            uri = 'digitaltwins/{}/components/{}' \
            .format(self._dtid, self._component_path)

        return self.request(uri, method, body=json.dumps(self.update_process))

    def _get_body(self, op, key, value=None):
        opt = {'op': op, 'path': '/' + key}
        
        if value != None:
            opt['value'] = value        

        return opt
