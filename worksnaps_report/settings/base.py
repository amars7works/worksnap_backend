import os
from celery.schedules import crontab

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'graphene_django',
    'reports',
    'reports_2',
    's7_auth',
    'summary_report',
    'time_entry',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'worksnaps_report.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'worksnaps_report.wsgi.application'

# User model
# AUTH_USER_MODEL = 's7_users.User'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/staticfiles/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, "/static"),
#)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'utils.exempt.CsrfExemptSessionAuthentication',
	)
}

AUTHENTICATION_BACKENDS = (
    # 'social_core.backends.open_id.OpenIdAuth',  # for Google authentication
    # 'social_core.backends.google.GoogleOpenId',  # for Google authentication
    # 'social_core.backends.google.GoogleOAuth2',  # for Google authentication
    # 'social_core.backends.google.GoogleOAuth',  # for Google authentication
    # 'social_core.backends.github.GithubOAuth2',  # for Github authentication
    # 'social_core.backends.facebook.FacebookOAuth2',  # for Facebook authentication
    # 'social_core.backends.twitter.TwitterOAuth',  # for twitter authentication
    'django.contrib.auth.backends.ModelBackend',
    's7_auth.authentication.EmailAuthBackend'
)


# REDIS related settings 
#REDIS_HOST = 'ec2-13-233-35-20.ap-south-1.compute.amazonaws.com'
#REDIS_PORT = '6379'
#BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
#BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600} 
#CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'

#Celery Broker
#CELERY_BROKER_URL = 'amqp://ec2-13-233-35-20.ap-south-1.compute.amazonaws.com'

#app.conf.beat_schedule = {
#    'send-report-every-single-minute': {
#        'task': 'publish.tasks.send_view_count_report',
#        'schedule': crontab(minute='*/5'),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at m$
#    },
#}
