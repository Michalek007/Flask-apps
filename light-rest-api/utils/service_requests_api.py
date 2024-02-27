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

    def kill(self):
        return self.get('/kill/')

    def restart(self):
        return self.get('/restart/')

    def performance(self):
        return self.get('/performance/')

    def add_params(self, cpu_usage, disk_usage, memory_usage):
        return self.post('/add_params/', params=dict(
            CpuUsage=cpu_usage,
            DiskUsage=disk_usage,
            MemoryUsage=memory_usage
        ))
