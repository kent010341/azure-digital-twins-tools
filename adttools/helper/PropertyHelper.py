import requests
import json
from .RequestHelper import RequestHelper

class PropertyHelper(RequestHelper):

    def __init__(self, host_name, token_path=None, token=None):
        super().__init__(host_name, token_path, token)
        self.__is_preparing_p = False
        self.__is_preparing_c = False
        self.__is_preparing_r = False

    def get_twin_detail(self, dtid):
        method = requests.get
        uri = 'digitaltwins/{}'.format(dtid)

        return self.request(uri, method)

    def prepare_property(self, dtid):
        assert not (self.__is_preparing_c or self.__is_preparing_r), \
            'The process has already start for updating another.'

        self.__dtid = dtid
        self.__update_process = list()
        self.__is_preparing_p = True

        return self

    def prepare_component(self, dtid, component_path):
        assert not (self.__is_preparing_p or self.__is_preparing_r), \
            'The process has already start for updating another.'

        self.__dtid = dtid
        self.__component_path = component_path
        self.__update_process = list()
        self.__is_preparing_c = True

        return self

    def prepare_relationship(self, source, rid):
        assert not (self.__is_preparing_p or self.__is_preparing_c), \
            'The process has already start for updating another.'

        self.__dtid = source
        self.__rid = rid
        self.__update_process = list()
        self.__is_preparing_r = True

        return self

    def update_property(self, key, value):
        assert self.__is_preparing_p or self.__is_preparing_c, \
            'The method \'update_property\' can\'t be used without using the method \'prepare\' before.'

        self.__update_process.append(self.__get_body('replace', key, value))

        return self

    def add_property(self, key, value):
        assert self.__is_preparing_p or self.__is_preparing_c, \
            'The method \'update_property\' can\'t be used without using the method \'prepare\' before.'

        self.__update_process.append(self.__get_body('add', key, value))

        return self

    def remove_property(self, key):
        assert self.__is_preparing_p or self.__is_preparing_c, \
            'The method \'update_property\' can\'t be used without using the method \'prepare\' before.'
            
        self.__update_process.append(self.__get_body('remove', key))
        
        return self

    def submit(self):
        method = requests.patch
        if self.__is_preparing_p:
            uri = 'digitaltwins/{}'.format(self.__dtid)
        elif self.__is_preparing_c:
            uri = 'digitaltwins/{}/components/{}' \
            .format(self.__dtid, self.__component_path)
        elif self.__is_preparing_r:
            uri = 'digitaltwins/{}/relationships/{}' \
            .format(self.__dtid, self.__rid)

        return self.request(uri, method, body=json.dumps(self.__update_process))

    def __get_body(self, op, key, value=None):
        opt = {'op': op, 'path': '/' + key}
        
        if value != None:
            opt['value'] = value        

        return opt
