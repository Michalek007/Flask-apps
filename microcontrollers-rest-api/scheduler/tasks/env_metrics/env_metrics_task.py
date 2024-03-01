from scheduler.tasks import TaskBase


class EnvMetricsTask(TaskBase):
    """ main_task -> makes post requests add_env_metrics to service """

    def main_task(self):
        self.add_env_metrics()

    def add_env_metrics(self):
        # TODO: implement
        pass
