""" APScheduler object and scheduler jobs.
    Usage:
        from app.periodic_tasks import deploy_scheduler
        deploy_scheduler()
    Important: should be used before running Flask app
"""
from flask_apscheduler import APScheduler
import psutil
from datetime import datetime

from app import app, db
from database.schemas import Performance
from utils import ServiceRequestsApi

scheduler = APScheduler()


@scheduler.task("cron", id="save_performance", minute="*")
def save_performance():
    # # saving performance in db without making request to api
    # parameters = Performance(timestamp=str(datetime.now()), memory_usage=psutil.virtual_memory()[2],
    #                          cpu_usage=psutil.cpu_percent(0.5), disk_usage=psutil.disk_usage('/')[3])
    # with app.app_context():
    #     db.session.add(parameters)
    #     db.session.commit()

    # # saving performance in db with first get, then post request
    service_api = ServiceRequestsApi()
    response = service_api.performance()
    if response is None:
        return
    data = response.json()

    response = service_api.add_params(
        cpu_usage=data['cpu']['usage'],
        disk_usage=data['disk']['usage'],
        memory_usage=data['virtual_memory']['usage'])
    if response is None:
        return

    print("Performance saved!")


def deploy_scheduler():
    """ Deploys scheduler. Should be called before running app. """
    scheduler.init_app(app)
    scheduler.start()
    print("Scheduler deployed!")
