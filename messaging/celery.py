from __future__ import absolute_import
import os
import datetime
from celery import Celery
from celery.schedules import crontab
from django.conf import settings


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging.settings')
app = Celery('messaging')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
  print('Request: {0!r}'.format(self.request))


app.conf.beat_schedule = {
    'add-every-minute-contrab': {
        'task': 'send_notification',
        'schedule': crontab(),
    }
}