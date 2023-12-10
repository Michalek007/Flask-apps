from client.errors import ErrorMonitor, ErrorType
from utils import ServiceRequestsApi


class ServiceRequestsApiAdapter:
    """ Adapter for ServiceRequestsApi class.
        Implements error handling.
    """
    def __init__(self, api: ServiceRequestsApi):
        self.api = api
        self.err_monitor = ErrorMonitor()

    def get_pid(self):
        response = self.api.get_pid()
        err = self.err_monitor.request(response, 'Getting service pids')
        if err:
            self.err_monitor.report_error(client_error=err)
            return None
        return response

    def set_pid(self, pid):
        response = self.api.set_pid(pid)
        err = self.err_monitor.request(response, 'Setting client pid')
        if err:
            self.err_monitor.report_error(client_error=err)
            return False
        return True

    def protected(self):
        return self.api.protected()
