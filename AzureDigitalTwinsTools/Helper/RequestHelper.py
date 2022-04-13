class RequestHelper:

    def __init__(self, token_path, host_name):
        self.__read_token(token_path)
        self.__host_name = host_name

    def request(self, uri, method, uri_params=None, body=None):
        url = self.__get_url(uri, uri_params)
        response = method(url, data=body, headers=self.__get_headers())
        response.raise_for_status()

        return response

    def __read_token(self, path):
        opt = ''
        with open(path, 'r') as f:
            opt = f.read()

        assert opt != '', 'Token is empty.'

        self.__token = 'Bearer ' + opt

    def __get_headers(self):
        return {
            'Content-Type': 'application/json', 
            'Authorization': self.__token
        }

    def __get_url(self, uri, params):
        opt = 'https://{}/{}?api-version=2020-10-31'.format(self.__host_name, uri)

        if params != None:
            if isinstance(params, str):
                opt += '&' + params
            else:
                for param in params:
                    opt += '&' + param

        return opt
