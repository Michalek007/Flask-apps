from app import app, bcrypt, db
from utils import ServiceRequestsApi


@app.cli.command('app_kill')
def app_kill():
    """ Shuts down server. """
    service_api = ServiceRequestsApi()
    service_api.kill()
    print('Service is shut down!')


@app.cli.command('app_restart')
def app_restart():
    """ Restarts server. """
    service_api = ServiceRequestsApi()
    service_api.restart()
    print('Service is restarting!')
