""" Internal client. """

from apscheduler.schedulers.blocking import BlockingScheduler

from client.core import Client
from utils import ServiceRequestsApi
from configuration import ProductionConfig, DevelopmentConfig, TestingConfig


def create_client():
    """ Creates database, api and client objects.
        Returns client.
    """

    # TODO: implement -> database object for client
    db = None
    api = ServiceRequestsApi()
    scheduler = BlockingScheduler()

    client = Client(scheduler=scheduler,
                    api=api,
                    database=db)
    return client
