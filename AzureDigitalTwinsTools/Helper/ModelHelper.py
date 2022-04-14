import requests
import json
from .RequestHelper import RequestHelper

class ModelHelper(RequestHelper):

    def __init__(self, token_path, host_name):
        super().__init__(token_path, host_name)
        self.__component_dict = {}

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

        curr_model = model
        is_searching = True
        curr_component_dict = {}

        while is_searching:
            curr_component_dict[curr_model] = []

            if dict_models[curr_model].get('contents') != None:
                curr_component_dict = self.__append_component(
                    curr_component_dict, dict_models[curr_model]['contents'], curr_model)

            if dict_models[curr_model].get('extends') != None:
                # find parent
                curr_model = dict_models[curr_model]['extends']

                # check if the parent has searched, if so, add to the list
                if self.__component_dict.get(curr_model) != None:
                    curr_component_dict = self.__append_with_found(
                        curr_component_dict, curr_model)
                    is_searching = False
            else:
                is_searching = False

        self.__store_to_dict(curr_component_dict)

        return curr_component_dict

    def __append_component(self, curr_component_dict, contents, curr_model):
        for content in contents:
            if content['@type'] == 'Component':
                cname = content['name']
                for k in curr_component_dict.keys():
                    curr_component_dict[k].append(cname)

        return curr_component_dict

    def __append_with_found(self, curr_component_dict, parent):
        parent_component = self.__component_dict[parent]

        for k in curr_component_dict.keys():
            curr_component_dict[k] += parent_component

        return curr_component_dict

    def __store_to_dict(self, curr_component_dict):
        # curr_component_dict + self.__component_dict
        for k, v in curr_component_dict.items():
            self.__component_dict[k] = v
