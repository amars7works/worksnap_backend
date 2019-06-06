#!/usr/bin/env python
import os
import sys

from decouple import config

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        os.environ.setdefault('DJANGO_EXECUTION_ENVIRONMENT', 'LOCAL')
        print('Current environment set to local')

if __name__ == "__main__":
    '''
	This is tells django which settings file to use, depending on
	the value of the DJANGO_EXECUTION_ENVIRONMENT variable.
    '''
    DJANGO_EXECUTION_ENVIRONMENT=get_env_variable('DJANGO_EXECUTION_ENVIRONMENT')

    if DJANGO_EXECUTION_ENVIRONMENT == 'PRODUCTION':
        print('Environment: Production')
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "worksnaps_report.settings.production")
    elif DJANGO_EXECUTION_ENVIRONMENT == 'STAGING':
        print('Environment: Staging')
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "worksnaps_report.settings.staging")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "worksnaps_report.settings.local")

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
