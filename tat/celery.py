import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tat.settings')

app = Celery("proj")
# namespace celery indica que de conf use solo variables que tengan prefijo CELERY

app.config_from_object('django.conf:settings', namespace="CELERY")
# Load task modules from all registered django apps, each app should have a tasks.py module
app.autodiscover_tasks()

from celery.schedules import crontab

app.conf.beat_schedule = {
    'add-every-minute-contrab':{
        'task':'multiply_two_numbers',
        'schedule':crontab(),
        'args':(16,16)
    },
    'add-every-5-seconds':{
        'task':'multiply_two_numbers',
        'schedule':5.0,
        'args':(16,16)
    },
    

}
""" 'add-every-30-seconds':{
        'task':'multiply_two_numbers',
        'schedule':30.0,
        'args':(16,16)
    } """


@app.task(bind=True)
def debug_task(self):
    print(f"Request {self.request}")