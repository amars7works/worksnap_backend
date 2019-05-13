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
  'request_leave_mail': {
    'task':'reports_2.request_leave_mail', 'schedule':crontab()
  },
  'send_users_daily_reports_mail':{
    'task':'reports_2.send_users_daily_reports_mail','schedule':crontab()
  },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.office365.com'
EMAIL_HOST_USER = 'vikramp@s7works.io'
EMAIL_HOST_PASSWORD = 'vicky@116'
EMAIL_PORT = 587
