class RequestHelper:

    def __init__(self, host_name, token_path=None, token=None):
        if token_path != None:
            self.__read_token(token_path)
        elif token != None:
            self.__token = token
        else:
            raise ValueError('Either token_path or token should be given.')

        self.__host_name = host_name

    def request(self, uri, method, uri_params=None, body=None):
        url = self.__get_url(uri, uri_params)
        response = method(url, data=body, headers=self.__get_headers())
        response.raise_for_status()

        return response

    def get_token(self):
        return self.__token

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
