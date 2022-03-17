import uuid

class RequestHelper:

    def __init__(self, token_path, host_name):
        self._read_token(token_path)
        self.host_name = host_name

    def request(self, uri, method, uri_params=None, body=None):
        url = self._get_url(uri, uri_params)
        response = method(url, data=body, headers=self._get_headers())
        self._assert_resp(response)

        return response

    def _read_token(self, path):
        opt = ''
        with open(path, 'r') as f:
            opt = f.read()

        assert opt != '', 'Token is empty.'

        self._token = 'Bearer ' + opt

    def _get_headers(self):
        return {
            'Content-Type': 'application/json', 
            'Authorization': self._token
        }

    def _get_url(self, uri, params):
        opt = 'https://{}/{}?api-version=2020-10-31'.format(self.host_name, uri)

        if params != None:
            if isinstance(params, str):
                opt += '&' + params
            else:
                for param in params:
                    opt += '&' + param

        return opt

    def _assert_resp(self, response):
        assert str(response.status_code)[0] == '2', \
                'status code not 2xx ({})'.format(response.status_code)

