"""
WSGI config for double_critical project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from decouple import config
requires_system_checks = False


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        os.environ.setdefault('DJANGO_EXECUTION_ENVIRONMENT', 'LOCAL')

'''
   This tells django which settings file to use, depending on 
   the value of the DJANGO_EXECUTION_ENVIRONMENT variable.
'''
DJANGO_EXECUTION_ENVIRONMENT = get_env_variable('DJANGO_EXECUTION_ENVIRONMENT')

if DJANGO_EXECUTION_ENVIRONMENT == 'STAGING':
    print('Environment: Staging')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'worksnaps_report.settings.staging')
elif DJANGO_EXECUTION_ENVIRONMENT == 'PRODUCTION':
    print('Environment: Production')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'worksnaps_report.settings.production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'worksnaps_report.settings.local')

application = get_wsgi_application()
