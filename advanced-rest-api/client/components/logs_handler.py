from datetime import datetime, timedelta

from client.components.component_base import ComponentBase


class LogsHandler(ComponentBase):
    """ Implements methods related to logs handling. """
    def main_method(self):
        """ Deletes client & service logs older than week ago. """
        timestamp = datetime.now() - timedelta(days=7)

        output = self.api.delete_logs(name='client', timestamp=timestamp)
        if output:
            self.config.update_client_status(f'Client logs older than {timestamp} deleted successfully. ')

        output = self.api.delete_logs(name='service', timestamp=timestamp)
        if output:
            self.config.update_client_status(f'Service logs older than {timestamp} deleted successfully. ')
