import logging
from datetime import datetime

from configuration import Config


class ClientConfig:
    """ Implements methods used in whole client package.
        Accessible for both client core and component classes.
        Singleton implementation.
        Attributes:
            api: ServiceRequestsApi object
    """
    api = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ClientConfig, cls).__new__(cls)
        return cls.instance

    def update_client_status(self, status: str, message: str = None):
        """ Updates client status in service. """
        self.api.set_client_status(status=status)
        if not message:
            message = status
        logging.info(message)
        print(message)

    @staticmethod
    def get_self_software():
        """ Returns current DM software. """
        project_details = Config.get_project_details().metadata
        major, minor, release, build = map(int, project_details.VERSION.split("."))
        return project_details.PROJECT_NAME, major, minor, release, build
