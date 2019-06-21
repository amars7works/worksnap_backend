from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'qu6d=)fywmp_+%3dj2q6!dj=ez36a!-$r%1wknp8mh%=96p1am'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

SECRET_KEY = '4rq1*w#u!4ew5f-d7+xa#x4ne12*clbw7921csz#0u8wa_yvm$'

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR,'db.sqlite3'),
  }
}

CELERY_BEAT_SCHEDULE = {
  'send-report-every-single-minute': {
    'task': 'reports.get_users_data', 'schedule':crontab(minute=10,hour=1),
  },
  'update-employee-leaves': {
    'task':'reports_2.update_employee_leaves', 'schedule':crontab(0,3,day_of_month='1')
  },
  'send_users_daily_reports_mail':{
    'task':'reports.send_users_daily_reports_mail','schedule':crontab()
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

CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_TIMEZONE = 'Asia/Kolkata'


# Send request/report emails to
EMPLOYER_EMAIL = ['amars@s7works.io']
EMPLOYER_NAME = 'Admin'
MANAGER_EMAIL_PROJECT_ONE = ['manis@s7works.io']
MANAGER_EMAIL_PROJECT_TWO = ['vikramp@s7works.io']
