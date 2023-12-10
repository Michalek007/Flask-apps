from enum import Enum
import json


class ErrorLevel(Enum):
    LOW = 0  # updates client status, prints error
    MEDIUM = 1  # updates client status, prints and logs error
    HIGH = 2  # updates client status, prints and logs error, and <specific_action>


class ErrorType(Enum):
    RequestsException = 0
    RequestStatusCode400 = 1
    RequestStatusCode500 = 2


class ClientError:
    """ Implements client related errors. """
    def __init__(self, error_type: ErrorType,
                 content: str = None,
                 aborted_action: str = None,
                 level: ErrorLevel = ErrorLevel.LOW):

        self.error_type = error_type
        self.content = content
        self.aborted_action = aborted_action
        self.level = level

    def get_error_msg(self):
        """ Returns ErrorMsg object. """
        return json.dumps(dict(err_type=self.error_type.name, content=self.content, aborted_action=self.aborted_action))
