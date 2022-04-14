import requests
import json
from .RequestHelper import RequestHelper
from .ModelHelper import ModelHelper

class TwinHelper(RequestHelper):

    def __init__(self, token_path, host_name):
        super().__init__(token_path, host_name)
        self.__mh = ModelHelper(token_path, host_name)
        self.__found_component = {}
        
    ##
    # Add a digital twin with specified model ID, the initial value of 
    # properties and component can be set by using dictionary.
    # 
    # dtid (str): digital twin ID
    # model (str): dtmi (digital twins model ID)
    # init_property (dict): initial value given to the properties
    #     should look like {"p_1": 123, "p_2":{"sub_p_1": "some value"}}
    # init_component (dict): initial value given to the components
    #     should look like {"c_1": {"c_1_property": "some value"}}
    ##
    def add_twin(self, dtid, model, init_property={}, init_component={}):
        # https://docs.microsoft.com/en-us/rest/api/digital-twins/dataplane/twins/digitaltwins_add
        method = requests.put
        uri = 'digitaltwins/{}'.format(dtid)
        body = self.__get_add_body(model, init_property, init_component)

        try:
            resp = self.request(uri, method, body=body)
        except:
            body = self.__get_add_body(model, init_property, init_component, search=True)
            resp = self.request(uri, method, body=body)

        return resp

    ##
    # Delete a digital twin with digital twin ID
    ##
    def delete_twin(self, dtid):
        # https://docs.microsoft.com/en-us/rest/api/digital-twins/dataplane/twins/digitaltwins_delete
        method = requests.delete
        uri = 'digitaltwins/{}'.format(dtid)

        return self.request(uri, method)

    def __get_add_body(self, model, init_property, init_component, search=False):
        body = {'$metadata': {'$model': model}}
        
        for k, v in init_property.items():
            body[k] = v

        if not search and not (model in self.__found_component.keys()):
            for k, v in init_component.items():
                component_value = v
                component_value['$metadata'] = {}
                body[k] = component_value
        else:
            try:
                component_list = self.__found_component[model]
            except:
                self.__found_component = self.__mh.find_model_components_list(model)
                component_list = self.__found_component[model]

            keys = init_component.keys()
            for c in component_list:
                v = init_component[c] if c in keys else {}

                component_value = v
                component_value['$metadata'] = {}
                body[c] = component_value

        return json.dumps(body)
