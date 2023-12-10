from abc import ABC, abstractmethod

from client.errors import ErrorMonitor, ClientError
from client.core.config import ClientConfig
from client.apis import ServiceRequestsApiAdapter


class ComponentBase(ABC):
    """ Base class for all components. """
    def __init__(self, api: ServiceRequestsApiAdapter, database):
        self.api = api
        self.db = database
        self.err_monitor = ErrorMonitor()
        self.config = ClientConfig()

    @abstractmethod
    def main_method(self):
        """ Method which will be called in client class.
            Should contain main functionalities of component.
        """
        pass
