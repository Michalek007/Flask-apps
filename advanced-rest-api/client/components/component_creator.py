from enum import Enum


class ComponentTypes(Enum):
    # add new component types here
    pass


class ComponentCreator:
    """ Contains factory method for components. """
    @staticmethod
    def create_component(api, database, scheduler, component_type: ComponentTypes):
        """ Factory method. """
        # if component_type == ComponentTypes.your_component:
        #     return YourComponent(api=api, database=database, scheduler=scheduler)
        # else:
        #     return None
        return None
