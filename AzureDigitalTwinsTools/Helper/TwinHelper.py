import requests
import json
import pandas as pd
from .RequestHelper import RequestHelper

class TwinHelper(RequestHelper):

    def __init__(self, token_path, host_name):
        super().__init__(token_path, host_name)
        
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
        body = self._get_add_body(model, init_property, init_component)

        return self.request(uri, method, body=body)

    ##
    # Delete a digital twin with digital twin ID
    ##
    def delete_twin(self, dtid):
        # https://docs.microsoft.com/en-us/rest/api/digital-twins/dataplane/twins/digitaltwins_delete
        method = requests.delete
        uri = 'digitaltwins/{}'.format(dtid)

        return self.request(uri, method)

    def _get_add_body(self, model, init_property, init_component):
        body = {'$metadata': {'$model': model}}
        
        for k, v in init_property.items():
            body[k] = v

        for k, v in init_component.items():
            component_value = v
            component_value['$metadata'] = {}
            body[k] = component_value

        return json.dumps(body)
