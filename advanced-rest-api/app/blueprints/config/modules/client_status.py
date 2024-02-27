from datetime import datetime


class ClientStatus:
    """ Implements stream-like object for client status. """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ClientStatus, cls).__new__(cls)
            cls.status_stream = []
        return cls.instance

    def set(self, status: str):
        """ Adds timestamp and appends status to stats_stream list.
            Args:
                status: string message
        """
        self.status_stream.append(str(datetime.now()) + ': ' + status)

    def get(self):
        """ Returns first item from status_stream list, and then removes it
            or None if stream is empty.
        """
        if not self.status_stream:
            return None
        return_value = self.status_stream[0]
        self.status_stream.remove(return_value)
        return return_value
