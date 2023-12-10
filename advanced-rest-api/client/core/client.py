import time
import os
import logging

from client.errors.error_monitor import ErrorMonitor
from client.components import ComponentCreator, ComponentTypes
from client.apis import ServiceRequestsApiAdapter
from client.core.config import ClientConfig


class Client:
    """ Client core class.

        Implements methods responsible for running scheduler, shutting down, checking connection etc.
        Responsible for creating components objects and calling main_method of each
        (as scheduler jobs or at the startup)

        Attributes:
            functionalities: components that will be used at the startup
            scheduler_jobs: components that will be added as scheduler jobs
    """
    def __init__(self, scheduler, api, database):
        self.scheduler = scheduler

        self.error_monitor = ErrorMonitor()
        ErrorMonitor.db = database

        self.config = ClientConfig()
        ClientConfig.api = api

        self.db = database
        self.api = ServiceRequestsApiAdapter(api=api)

        # when new functionality is needed, create new class in client/components (base class: ComponentBase)
        # and update factory method (ComponentCreator) then add correct ComponentType to one of these attributes:
        # self.functionalities -> main_method will be called once at the start of client before starting scheduler
        # self.scheduler_jobs -> main_method will be called periodically (interval time defined in minutes)

        self.functionalities = [
            # ComponentTypes.your_component
        ]

        self.scheduler_jobs = [
            # {
            #     'component_type': ComponentTypes.your_component,
            #     'id': ComponentTypes.your_component.name,
            #     'minutes': 5
            # },
        ]

    @staticmethod
    def shut_down(message: str = None):
        if message:
            print(message)
            logging.error(message)
        exit(-1)

    # public methods:
    def run(self):
        """ Starts scheduler. """
        self.config.update_client_status(status='Scheduler is running', message='*** Scheduler is running ***')
        self.scheduler.start()

    def startup(self):
        """ Actions that are made before starting scheduler. """
        result = self._wait_for_connection()
        if not result:
            self.shut_down()
        self._set_pid()

        for component_type in self.functionalities:
            component = ComponentCreator.create_component(self.api, self.db, self.scheduler, component_type)
            component.main_method()

        self._set_scheduler_jobs()

    # private methods:
    def _set_scheduler_jobs(self):
        """ Sets schedulers jobs before running scheduler. """

        for job in self.scheduler_jobs:
            component = ComponentCreator.create_component(self.api, self.db, self.scheduler, job.get('component_type'))
            self.scheduler.add_job(component.main_method, 'interval', id=job.get('id'), minutes=job.get('minutes'))

        self.scheduler.print_jobs()

    def _wait_for_connection(self, timeout=2):
        """ Check connection with api.
            Args:
                timeout: minutes, maximum waiting time for connection
            Returns:
                ``True`` if connection was established, ``False`` otherwise
        """
        i = 0
        while i < timeout * 60:
            response = self.api.protected()
            if response is None:
                print('Connection error. Check if server is running.')
            elif response.status_code == 401:
                logging.error('Unauthorized. Check if bearer token is correct.')
                return False
            elif response.status_code == 200:
                return True
            i += 1
            time.sleep(1)
        return False

    def _set_pid(self):
        """ Sets client pid in service. If pid is already set, shuts down. """
        response = self.api.get_pid()
        data = response.json()
        client_pid = data["CLIENT"]
        if client_pid is not None:
            self.shut_down('Client is already running')
        self.api.set_pid(pid=os.getpid())
