from datetime import datetime

from scheduler.tasks import TaskBase
from database.schemas import Acceleration


class AccTask(TaskBase):
    """ main_task -> adds computer performance to database """

    def main_task(self):
        print('Not implemented yet!')
