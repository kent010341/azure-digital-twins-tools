import requests
import json
from .RequestHelper import RequestHelper

# https://docs.microsoft.com/zh-tw/azure/digital-twins/how-to-query-graph
class QueryHelper(RequestHelper):

    def __init__(self, self, token_path, host_name):
        super().__init__(token_path, host_name)

    def begin(self):
        self.__query = 'SELECT * FROM digitaltwins WHERE '

    def add_condition(self, condition):

    def add_relationship(self, relationship):

    def commit(self):
        return self.run_query(self.__query)

    def run_query(self, query):
        method = requests.post
        uri = 'query'

        body = '{"query":"' + query + '"}'

        return self.request(uri, method, body=body)
