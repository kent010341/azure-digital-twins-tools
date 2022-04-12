import requests
import json
from copy import deepcopy
from .RequestHelper import RequestHelper

class ModelHelper(RequestHelper):

    def __init__(self, token_path, host_name):
        super().__init__(token_path, host_name)

    def list_models(self, model=None):
        method = requests.get
        uri = 'models'

        if model != None:
            uri_params = 'dependenciesFor={}&includeModelDefinition=True'.format(model)
        else:
            uri_params = 'includeModelDefinition=True'

        resp = self.request(uri, method, uri_params=uri_params).text

        return json.loads(resp)['value']

    def find_model_components_list(self, model):
        related_models = self.list_models(model)

        dict_models = {}
        for m in related_models:
            dict_models[m['id']] = m['model']

        component_list = []
        curr_model = model
        has_parent = True

        # print(dict_models[curr_model])
        # print(type(dict_models[curr_model]))

        while has_parent:
            try:
                contents = dict_models[curr_model]['contents']
                for content in contents:
                    if content['@type'] == 'Component':
                        component_list.append(content['name'])
            except:
                pass

            try:
                curr_model = dict_models[curr_model]['extends']
            except:
                has_parent = False

        return component_list
