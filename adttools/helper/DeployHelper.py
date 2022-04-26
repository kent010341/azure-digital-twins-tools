import json
import pandas as pd
from .RelationshipHelper import RelationshipHelper
from .TwinHelper import TwinHelper
from .QueryHelper import QueryHelper

class DeployHelper:

    def __init__(self, host_name, token_path=None, token=None):
        self.__rh = RelationshipHelper(
            host_name=host_name, token_path=token_path, token=token)
        self.__th = TwinHelper(host_name=host_name, token=self.__rh.get_token())
        self.__qh = QueryHelper(host_name=host_name, token=self.__rh.get_token())

    ##
    # Deploy digital twins with a csv file.
    # The columns should be 'modelid', 'dtid', 'init_property', 'init_component', 'rname', 'rtarget', 'init_rproperty'
    # 'init_property', 'init_component' and 'init_rproperty' are optional columns.
    #     'modelid': model ID
    #     'dtid': Twin ID
    #     'init_property': (JSON format) Can be empty, the initial value of properties
    #     'init_component': (JSON format) Can be empty, the initial value of components
    #     'rname': Relationship name, if 'rname' is specified, 'rtarget' is required.
    #              If multiple relationships are required, just add a new line without 'modelid' and using an existing 'dtid'.
    #     'rtarget': Target twin ID if a relationship is specified
    #     'init_rproperty': Initial value of properties of relationship if a relationship is specified.
    ##
    def csv_deploy(self, path, atomic=True):
        # read csv
        df = pd.read_csv(path)

        # a list for relationships, used for creating relationships after twins are creating.
        relationships_storage = list()

        # used for making this process atomic, if something failed, remove all things in these two list
        if atomic:
            succeed_twins = list()
            succeed_relationships = list()
        else:
            failed_twins = list()
            failed_relationships = list()

        # check if optional columns exist
        has_init_property = False
        has_init_component = False
        has_init_rproperty = False

        for c in df.columns:
            if c == 'init_property':
                has_init_property = True
            elif c == 'init_component':
                has_init_component = True
            elif c == 'init_rproperty':
                has_init_rproperty = True

        for _, row in df.iterrows():
            modelid = row['modelid']
            dtid = row['dtid']

            # check empty data
            if not has_init_property or pd.isna(row['init_property']):
                init_property = {}
            else:
                init_property = json.loads(row['init_property'])

            if not has_init_component or pd.isna(row['init_component']):
                init_component = {}
            else:
                init_component = json.loads(row['init_component'])

            if not has_init_rproperty or pd.isna(row['init_rproperty']):
                init_rproperty = {}
            else:
                init_rproperty = json.loads(row['init_rproperty'])

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
                    if atomic:
                        succeed_twins.append(dtid)
                except Exception as e:
                    print('Exception:', e)
                    if atomic:
                        self.__atomic(succeed_twins)
                        return None
                    else:
                        failed_twins.append(
                            (modelid, dtid, init_property, init_component))

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
                if atomic:
                    succeed_relationships.append((r[0], rid))
            except Exception as e:
                print('Exception:', e)
                if atomic:
                    self.__atomic(succeed_twins, succeed_relationships)
                    return None
                else:
                    failed_relationships.append(r)

        if not atomic and (failed_twins or failed_relationships):
            print('\'atomic\' is False, start creating csv with failed twins and relationships.')
            self.__failed_csv(path, failed_twins, failed_relationships)

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

    def __failed_csv(self, csv_path, failed_twins, failed_relationships):
        csv_data = {
            'modelid': [],
            'dtid': [],
            'init_property': [],
            'init_component': [],
            'rname': [],
            'rtarget': []
        }

        for t in failed_twins:
            csv_data['modelid'].append(t[0])
            csv_data['dtid'].append(t[1])

            if len(t[2]) != 0:
                csv_data['init_property'].append(
                    json.dumps(t[2], ensure_ascii=False))
            else:
                csv_data['init_property'].append(None)

            if len(t[3]) != 0:
                csv_data['init_component'].append(
                    json.dumps(t[3], ensure_ascii=False))
            else:
                csv_data['init_component'].append(None)
            
            csv_data['rname'].append(None)
            csv_data['rtarget'].append(None)

            print('Add failed twin: modelid={}, dtid={}, init_property={}, init_component={}'.format(
                t[0], t[1], t[2], t[3]
            ))

        for r in failed_relationships:
            csv_data['modelid'].append(None)
            csv_data['dtid'].append(r[0])
            csv_data['init_property'].append(None)
            csv_data['init_component'].append(None)
            csv_data['rname'].append(r[2])
            csv_data['rtarget'].append(r[1])

            print('Add failed relationship: dtid={}, rtarget={}, rname={}'.format(
                r[0], r[1], r[2]
            ))

        df = pd.DataFrame(csv_data)
        opt_path = csv_path[:-len('.csv')] + '_failed.csv'
        df.to_csv(opt_path, index=False)

        print('File saved, path:', opt_path)
