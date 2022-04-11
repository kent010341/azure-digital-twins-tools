import json
import pandas as pd
from .RelationshipHelper import RelationshipHelper
from .TwinHelper import TwinHelper
from .QueryHelper import QueryHelper

class DeployHelper:

    def __init__(self, token_path, host_name):
        self.__rh = RelationshipHelper(token_path, host_name)
        self.__th = TwinHelper(token_path, host_name)
        self.__qh = QueryHelper(token_path, host_name)

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
    def csv_deploy(self, path, atomic=True):
        # read csv
        df = pd.read_csv(path)

        # a list for relationships, used for creating relationships after twins are creating.
        relationships_storage = list()

        # used for making this process atomic, if something failed, remove all things in these two list
        succeed_twins = list()
        succeed_relationships = list()

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
                try:
                    self.__th.add_twin(
                        dtid=dtid, 
                        model=modelid, 
                        init_property=init_property, 
                        init_component=init_component
                    )
                    print('Add DT: dtid={}, modelid={}'.format(dtid, modelid))
                    succeed_twins.append(dtid)
                except:
                    if atomic:
                        self.__atomic(succeed_twins)
                    return

            # avoid adding relationship before the target is created, store it first
            if not pd.isna(rtarget) and not pd.isna(rname):
               relationships_storage.append((dtid, rtarget, rname))

        for r in relationships_storage:
            try:
                resp = self.__rh.add_relationship(
                    source=r[0], 
                    target=r[1], 
                    rname=r[2]
                ).text

                rid = json.loads(resp)['$relationshipId']

                print('Add relationship: source={}, target={}, relationship_name={}, relationship_id={}'
                    .format(r[0], r[1], r[2], rid))
                succeed_relationships.append((r[0], rid))
            except:
                if atomic:
                    self.__atomic(succeed_twins, succeed_relationships)
                return

    def clear(self):
        rs = self.__qh.query_relationships()
        for r in rs:
            self.__rh.delete_relationship(
                source=r['$sourceId'],
                rid=r['$relationshipId']
            )
            print('Delete relationship: source={}, relationship_id={}'
                .format(r['$sourceId'], r['$relationshipId']))

        twins = self.__qh.query_twins()
        for twin in twins:
            self.__th.delete_twin(dtid=twin['$dtId'])
            print('Delete twin:', twin['$dtId'])

    def __atomic(self, succeed_twins, succeed_relationships=[]):
        print('Something went wrong, start deleting twins and relationships created with this file.')
        for r in succeed_relationships:
            self.__rh.delete_relationship(
                source=r[0],
                rid=r[1]
            )
            print('Delete relationship: source={}, relationship_id={}'
                .format(r[0], r[1]))

        for dtid in succeed_twins:
            self.__th.delete_twin(dtid=dtid)
            print('Delete twin:', dtid)
