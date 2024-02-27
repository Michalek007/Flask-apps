import requests
import logging

from configuration import Config


class ServiceRequestsApi:
    """ Allows making requests to service.
        Contains methods for specific request with same name as endpoint.
        Authorisation is handled via bearer token.
    """
    def __init__(self, host=Config.LISTENER['host'], port=Config.LISTENER['port'], bearer_token=Config.TOKEN):
        self.headers = {'Authorization': f'Bearer {bearer_token}'}
        self.server_name = f'http://{host}:{port}'

    def post(self, url: str, params: dict = None):
        """ Makes post request.
            Args:
                url: url string in format /<url>/
                params: dict of query args
            Returns:
                request.Response object or ``None`` if error occurs
        """
        url = self.server_name + url
        try:
            response = requests.post(url, headers=self.headers, params=params)
        except (requests.ConnectionError, requests.ConnectTimeout, requests.RequestException) as error:
            logging.error(error)
            return None
        return response

    def get(self, url: str, params: dict = None):
        """ Makes get request.
            Args:
                url: url string in format /<url>/
                params: dict of query args
            Returns:
                request.Response object or ``None`` if error occurs
        """
        url = self.server_name + url
        try:
            response = requests.get(url, headers=self.headers, params=params)
        except (requests.ConnectionError, requests.ConnectTimeout, requests.RequestException) as error:
            logging.error(error)
            return None
        return response

    def set_pid(self, pid):
        return self.post('/set_pid/', dict(client=pid))

    def get_pid(self):
        return self.get('/get_pid/')

    def protected(self):
        return self.get('/protected/')

    def set_client_status(self, status: str):
        return self.get('/set_client_status/', dict(status=status))

    def get_logs(self, name: str):
        return self.get(f'/get_logs/{name}/')

    def delete_logs(self, name: str, timestamp):
        return self.get(f'/delete_logs/{name}/', dict(timestamp=timestamp))
