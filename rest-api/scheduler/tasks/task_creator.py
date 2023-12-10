from enum import Enum

from scheduler.tasks.performance import PerformanceTask


class TaskType(Enum):
    Performance = 0
    # add new task types here


class TaskCreator:
    """ Contains factory method for tasks. """
    @staticmethod
    def create_task(scheduler, api, database, task_type: TaskType):
        """ Factory method. """
        if task_type == TaskType.Performance:
            return PerformanceTask(scheduler=scheduler, api=api, database=database)
        else:
            return None
