from enum import Enum

from client.components.logs_handler import LogsHandler


class ComponentTypes(Enum):
    LogsHandler = 0
    # add new component types here
    pass


class ComponentCreator:
    """ Contains factory method for components. """
    @staticmethod
    def create_component(api, database, scheduler, component_type: ComponentTypes):
        """ Factory method. """
        if component_type == ComponentTypes.LogsHandler:
            return LogsHandler(api=api, database=database)
        # add conditions for new components here
        else:
            return None
