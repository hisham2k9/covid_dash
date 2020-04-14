from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from data_updater import india_data_api


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(india_data_api.update_india_data, 'interval', minutes=10)
    scheduler.start()
