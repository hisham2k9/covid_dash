from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from dash import data_scheduler


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(data_scheduler.mainman, 'interval', minutes=2)
    scheduler.start()
    