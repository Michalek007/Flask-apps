from datetime import datetime
import logging
import requests

from client.errors.client_error import ClientError, ErrorLevel, ErrorType
from client.core.config import ClientConfig


class ErrorMonitor:
    """ Implements errors handling & reporting methods.
        Singleton implementation.
        Attributes:
            db: database object
            config: ClientConfig object
    """
    db = None
    config = ClientConfig()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ErrorMonitor, cls).__new__(cls)
        return cls.instance

    def report_error(self, client_error: ClientError):
        """ Updates client status, logs or saves in database depends on error level
            Args:
                client_error: ClientError object
        """
        err_msg = client_error.get_error_msg()

        if client_error.error_type != ErrorType.RequestsException:
            self.config.update_client_status(status=err_msg)

        if client_error.level == ErrorLevel.MEDIUM:
            logging.error(err_msg)

        if client_error.level == ErrorLevel.HIGH:
            logging.error(err_msg)
            # TODO: implement saving in database or another specific action

    @staticmethod
    def request(response: requests.Response, action: str, level: ErrorLevel = ErrorLevel.MEDIUM):
        """ Error handling for request response.
            Args:
                 response: requests.Response object
                 action: name of the current action
                 level: error level
            Returns:
                specific ClientError object or ``None`` when no error occur
        """
        if response is None:
            return ClientError(
                error_type=ErrorType.RequestsException,
                content=None,
                aborted_action=action,
                level=level)
        elif 400 <= response.status_code < 500:
            return ClientError(
                error_type=ErrorType.RequestStatusCode400,
                content=response.json()['message'],
                aborted_action=action,
                level=level)
        elif 500 <= response.status_code:
            return ClientError(
                error_type=ErrorType.RequestStatusCode500,
                content='Internal service error.',
                aborted_action=action,
                level=level)
        else:
            return None
