from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'qu6d=)fywmp_+%3dj2q6!dj=ez36a!-$r%1wknp8mh%=96p1am'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


SECRET_KEY = '4rq1*w#u!4ew5f-d7+xa#x4ne12*cqerqwer42rf#0u8wa6yvm$'

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'worksnaps',
    'USER': 's7_worksnaps',
    'PASSWORD': 's7works.io',
    'HOST': 's7-internal.cluster-c7lti9kc1dov.ap-south-1.rds.amazonaws.com',
    'PORT': '3306',
  }
}

CELERY_BEAT_SCHEDULE = {
  'send-report-every-single-minute': {
    'task': 'reports.get_users_data', 'schedule':crontab(minute=10,hour=1),
  },
  'update-employee-leaves': {
    'task':'reports_2.update_employee_leaves', 'schedule':crontab(0,3,day_of_month=1)
  },
  'send_users_daily_reports_mail':{
    'task':'reports_2.send_users_daily_reports_mail','schedule':crontab(hour=22, day_of_week=6)
  },
}


# 'request_leave_mail': {
#   'task':'reports_2.request_leave_mail', 'schedule':crontab()
# },



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 's7works.smtp@gmail.com'
EMAIL_HOST_PASSWORD = 'smtpcode2112'
EMAIL_PORT = 587

CELERY_BROKER_URL = 'redis://ubuntu:worksnaps_2112@172.26.15.51:6379'
CELERY_RESULT_BACKEND = 'redis://ubuntu:worksnaps_2112@172.26.15.51:6379'
CELERY_TIMEZONE = 'Asia/Kolkata'

# Send request/report emails to
EMPLOYER_EMAIL = ['saumyag@s7works.io']
EMPLOYER_NAME = 'Saumya Garg'
MANAGER_EMAIL_PROJECT_ONE = ['manis@s7works.io']
MANAGER_EMAIL_PROJECT_TWO = ['dileepk@s7works.io']