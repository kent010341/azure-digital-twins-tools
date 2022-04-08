import requests
import uuid
import json
from .RequestHelper import RequestHelper
from .QueryHelper import QueryHelper

class RelationshipHelper(RequestHelper):

    def __init__(self, token_path, host_name):
        super().__init__(token_path, host_name)
        self.__qh = QueryHelper(token_path, host_name)

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
        return self.__qh.query_relationships(
            source=dtid, 
            target=target_dtid, 
            rname=relationship_name
        )

    def find_and_delete_relationships(self, dtid, relationship_name=None, target_dtid=None):
        rs = self.__qh.query_relationships(
            source=dtid, 
            target=target_dtid, 
            rname=relationship_name
        )

        for r in rs:
            self.delete_relationship(
                dtid=dtid,
                relationship_id=r['$relationshipId']
            )
