import psutil
from datetime import datetime

from scheduler.tasks import TaskBase
from database.schemas import Performance


class PerformanceTask(TaskBase):
    """ main_task -> adds computer performance to database """

    def main_task(self):
        # # saving performance in db without making request to api
        # parameters = Performance(timestamp=str(datetime.now()), memory_usage=psutil.virtual_memory()[2],
        #                          cpu_usage=psutil.cpu_percent(0.5), disk_usage=psutil.disk_usage('/')[3])
        # with self.scheduler.app.app_context():
        #     self.db.session.add(parameters)
        #     self.db.session.commit()
        #     print(Performance.query.all())

        # # saving performance in db with first get, then post request
        data = self.get_performance()
        if data is None:
            return

        response = self.api.add_params(cpu_usage=data[0], disk_usage=data[1], memory_usage=data[2])
        if response is None:
            return
        print("Performance saved!")

    def get_performance(self):
        response = self.api.performance()
        if response is None:
            return None
        data = response.json()
        return data['cpu']['usage'], data['disk']['usage'], data['virtual_memory']['usage']
