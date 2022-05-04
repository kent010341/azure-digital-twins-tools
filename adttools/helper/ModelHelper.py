import requests
import json
import os
import shutil
from .RequestHelper import RequestHelper

class ModelHelper(RequestHelper):

    def __init__(self, host_name, token_path=None, token=None):
        super().__init__(host_name, token_path, token)
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
                    curr_component_dict, 
                    dict_models[curr_model]['contents'], 
                    curr_model
                )

            # find parent
            curr_model = dict_models[curr_model].get('extends')
            if curr_model != None:
                # check if the parent has searched, if so, add to the list
                if self.__component_dict.get(curr_model) != None:
                    curr_component_dict = self.__append_with_found(
                        curr_component_dict, curr_model)
                    is_searching = False
            else:
                is_searching = False

        # update self.__component_dict
        self.__component_dict.update(curr_component_dict)

    def get_component_dict(self):
        return self.__component_dict

    def picker(self, model_folder, model_list, output_folder='picked'):
        self.__model_dict = self.__expand_folder(model_folder)
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        for model in model_list:
            if self.__model_dict.get(model) == None:
                print(model, 'not found.')
            else:
                self.__picked = list()
                self.__picking_model(model, output_folder)

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

    def __expand_folder(self, path):
        model_dict = dict()

        for root, _, files in os.walk(path):
            for file in files:
                model_detail = self.__read_dtdl(os.path.join(root, file))
                if model_detail != None:
                    model_dict[model_detail['modelid']] = model_detail

        return model_dict

    def __get_full_path(self, path, subfolder):
        sep = '' if path[-1] == '/' else '/'

        return path + sep + subfolder

    def __read_dtdl(self, path):
        if not path.endswith('.json'):
            return None

        with open(path, 'r') as f:
            dtdl = f.read()

        try:
            dtdl = json.loads(dtdl)
        except:
            print('Parsing DTDL failed. path:', path)
            return None

        depended_by = False
        modelid = dtdl['@id']
        extends = dtdl.get('extends', ()) # could be list, string, None

        if len(extends) != 0:
            depended_by = True

        if isinstance(extends, str):
            extends = [extends]

        rtarget = list()
        component = list()
        for content in dtdl.get('contents',()):
            # relationship target
            if content['@type'] == 'Relationship' and content.get('target') != None:
                rtarget.append(content['target'])
                depended_by = True
            elif content['@type'] == 'Component':
                component.append(content['schema'])
                depended_by = True

        return {
            'path': path,
            'modelid': modelid,
            'extends': extends,
            'component': component,
            'rtarget': rtarget,
            'depended_by': depended_by
        }

    def __picking_model(self, model, output_folder):
        if model in self.__picked:
            return None
        else:
            self.__picked.append(model)

        model_detail = self.__model_dict[model]
        shutil.copy2(model_detail['path'], output_folder)

        print('Add:', model)

        if model_detail['depended_by']:
            # extends
            for e in model_detail.get('extends'):
                self.__picking_model(e, output_folder)

            # component
            for c in model_detail['component']:
                self.__picking_model(c, output_folder)

            # rtarget
            for r in model_detail['rtarget']:
                self.__picking_model(r, output_folder)
