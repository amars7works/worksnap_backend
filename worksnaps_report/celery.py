from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        print("Set the %s environment variable" % (var_name))
        print("Current environment set to local")

'''
   This tells django which settings file to use, depending on 
   the value of the DJANGO_EXECUTION_ENVIRONMENT variable.
'''
DJANGO_EXECUTION_ENVIRONMENT = get_env_variable('DJANGO_EXECUTION_ENVIRONMENT')

if DJANGO_EXECUTION_ENVIRONMENT == 'STAGING':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "worksnaps_report.settings.staging")
elif DJANGO_EXECUTION_ENVIRONMENT == 'PRODUCTION':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "worksnaps_report.settings.production")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "worksnaps_report.settings.local")


app = Celery('worksnaps_report')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

#app.conf.beat_schedule = {
#    'send-report-every-single-minute': {
#        'task': 'publish.tasks.send_view_count_report',
#        'schedule': crontab(minute='*/5'),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
#    },
#}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

