import requests
import uuid
import json
from .RequestHelper import RequestHelper

class RelationshipHelper(RequestHelper):

    def __init__(self, token_path, host_name):
        super().__init__(token_path, host_name)

    def update_relationship(self):
        pass

    def list_relationships(self, dtid, relationship_name=None):
        # https://docs.microsoft.com/en-us/rest/api/digital-twins/dataplane/twins/digitaltwins_listrelationships
        method = requests.get
        uri = 'digitaltwins/{}/relationships'.format(dtid)

        return self.request(uri, method, uri_params=relationship_name)

    def add_relationship(self, dtid, target_dtid, relationship_name):
        # https://docs.microsoft.com/en-us/rest/api/digital-twins/dataplane/twins/digitaltwins_addrelationship
        method = requests.put
        uri = 'digitaltwins/{}/relationships/{}'.format(dtid, str(uuid.uuid4()))
        body = '{"$targetId": "' + target_dtid + \
                '","$relationshipName": "' + relationship_name + '"}'

        return self.request(uri, method, body=body)

    def delete_relationship(self, dtid, relationship_id):
        # https://docs.microsoft.com/en-us/rest/api/digital-twins/dataplane/twins/digitaltwins_deleterelationship
        method = requests.delete
        uri = 'digitaltwins/{}/relationships/{}'.format(dtid, relationship_id)

        return self.request(uri, method)

    def find_relationships_with_target(self, dtid, target_dtid, relationship_name=None):
        resp_content = self.list_relationships(dtid, relationship_name).content
        relationships = json.loads(resp_content)
        opt = list()

        for r in relationships['value']:
            if r['$targetId'] == target_dtid:
                opt.append({
                    'relationshipId': r['$relationshipId'],
                    'relationshipName': r['$relationshipName'],
                    'sourceId': r['$sourceId'],
                    'targetId': r['$targetId']
                })

        return opt

    def find_and_delete_relationships(self, dtid, relationship_name=None, target_dtid=None):
        resp_content = self.list_relationships(dtid, relationship_name).content
        relationships = json.loads(resp_content)

        if isinstance(target_dtid, str):
            target_dtid = [target_dtid]

        for r in relationships['value']:
            if target_dtid != None:
                for t in target_dtid:
                    if t == r['$targetId']:
                        self.delete_relationship(dtid, r['$relationshipId'])
            else:
                self.delete_relationship(dtid, r['$relationshipId'])
