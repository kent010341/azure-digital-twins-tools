import requests
import json
from .RequestHelper import RequestHelper
from .RelationshipHelper import RelationshipHelper
from .TwinHelper import TwinHelper

class DeployHelper(RequestHelper):

    def __init__(self, token_path, host_name):
        super().__init__(token_path, host_name)
        self.rh = RelationshipHelper(token_path, host_name)
        self.th = TwinHelper(token_path, host_name)

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
                self.th.add_twin(
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