import requests
import json
from .RequestHelper import RequestHelper

# https://docs.microsoft.com/zh-tw/azure/digital-twins/how-to-query-graph
class QueryHelper(RequestHelper):

    def __init__(self, host_name, token_path=None, token=None):
        super().__init__(host_name, token_path, token)

    def query_twins(self, dtid=None, condition=None):
        query = 'SELECT * FROM digitaltwins'

        if dtid != None or condition != None:
            query += ' WHERE'

        if dtid != None:
            query += ' $dtId=\'{}\''.format(dtid)
            if condition != None:
                query += ' AND'

        if condition != None:
            query += ' ({})'.format(condition)

        return self.run_query(query)

    def query_relationships(self, source=None, target=None, rname=None):
        query = 'SELECT * FROM relationships'

        if source != None or target != None or rname != None:
            query += ' WHERE'

        if source != None:
            query += ' $sourceId=\'{}\''.format(source)

        if target != None:
            query += ' $targetId=\'{}\''.format(target)

        if rname != None:
            query += ' $relationshipName=\'{}\''.format(rname)

        return self.run_query(query)

    def run_query(self, query):
        method = requests.post
        uri = 'query'
        body = '{"query":"' + query + '"}'

        resp = self.request(uri, method, body=body).text

        return json.loads(resp)['value']
