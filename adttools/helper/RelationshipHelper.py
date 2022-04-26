import requests
import uuid
import json
from .RequestHelper import RequestHelper
from .QueryHelper import QueryHelper

class RelationshipHelper(RequestHelper):

    def __init__(self, host_name, token_path=None, token=None):
        super().__init__(host_name, token_path, token)
        self.__qh = QueryHelper(host_name=host_name, token=self.get_token())

    def list_relationships(self, source, rname=None):
        # https://docs.microsoft.com/en-us/rest/api/digital-twins/dataplane/twins/digitaltwins_listrelationships
        method = requests.get
        uri = 'digitaltwins/{}/relationships'.format(source)

        return self.request(uri, method, uri_params=rname)

    def add_relationship(self, source, target, rname, init_property={}):
        # https://docs.microsoft.com/en-us/rest/api/digital-twins/dataplane/twins/digitaltwins_addrelationship
        method = requests.put
        uri = 'digitaltwins/{}/relationships/{}'.format(source, str(uuid.uuid4()))
        
        body = {'$targetId': target, '$relationshipName': rname}
        body.update(init_property)

        return self.request(uri, method, body=body)

    def delete_relationship(self, source, rid):
        # https://docs.microsoft.com/en-us/rest/api/digital-twins/dataplane/twins/digitaltwins_deleterelationship
        method = requests.delete
        uri = 'digitaltwins/{}/relationships/{}'.format(source, rid)

        return self.request(uri, method)

    def find_relationships_with_target(self, source, target, rname=None):
        return self.__qh.query_relationships(
            source=source, 
            target=target, 
            rname=rname
        )

    def find_and_delete_relationships(self, source, rname=None, target=None):
        rs = self.__qh.query_relationships(
            source=source, 
            target=target, 
            rname=rname
        )

        for r in rs:
            self.delete_relationship(
                source=source,
                rid=r['$relationshipId']
            )
