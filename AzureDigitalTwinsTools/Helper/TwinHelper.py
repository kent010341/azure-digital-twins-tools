import requests
import json
import pandas as pd
from .RequestHelper import RequestHelper
from .RelationshipHelper import RelationshipHelper

class TwinHelper(RequestHelper):

    def __init__(self, token_path, host_name):
        super().__init__(token_path, host_name)
        self.rh = RelationshipHelper(token_path, host_name)
        
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

    ##
    # Deploy digital twins with a csv file.
    # The columns should be 'modelid', 'dtid', 'init', 'rtarget', 'rname'
    #     'modelid': model ID
    #     'dtid': Twin ID
    #     'init_property': (JSON format) Can be empty, the initial value of properties
    #     'init_component': (JSON format) Can be empty, the initial value of components
    #     'rname': Relationship name, if 'rname' is specified, 'rtarget' is required.
    #              If multiple relationships are required, just add a new line without 'modelid' and using an existing 'dtid'.
    #     'rtarget': Target twin ID if a relationship is specified
    ##
    def csv_deploy(self, path):
        # read csv
        df = pd.read_csv(path)
        relationships_storage = list()

        for _, row in df.iterrows():
            modelid = row['modelid']
            dtid = row['dtid']

            if pd.isna(row['init_property']):
                init_property = {}
            else:
                init_property = json.loads(row['init_property'])

            if pd.isna(row['init_component']):
                init_component = {}
            else:
                init_component = json.loads(row['init_component'])

            rname = row['rname']
            rtarget = row['rtarget']

            if not pd.isna(modelid):
                self.add_twin(
                    dtid=dtid, 
                    model=modelid, 
                    init_property=init_property, 
                    init_component=init_component
                )
                print('Add DT: dtid={}, modelid={}'.format(dtid, modelid))

            # avoid adding relationship before the target is created, store it first
            if not pd.isna(rtarget) and not pd.isna(rname):
               relationships_storage.append((dtid, rtarget, rname))

        for r in relationships_storage:
            self.rh.add_relationship(
                dtid=r[0], 
                target_dtid=r[1], 
                relationship_name=r[2]
            )
            print('Add relationship: source={}, target={}, relationship_name={}'
                .format(r[0], r[1], r[2]))


    def _get_add_body(self, model, init_property, init_component):
        body = {'$metadata': {'$model': model}}
        
        for k, v in init_property.items():
            body[k] = v

        for k, v in init_component.items():
            component_value = v
            component_value['$metadata'] = {}
            body[k] = component_value

        return json.dumps(body)
