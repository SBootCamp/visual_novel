"""
Django settings for visual_novel project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import json

from kombu import Exchange, Queue

from django.core.exceptions import ImproperlyConfigured

# JSON-based secrets module
secrets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'secrets.json')
with open(secrets_path) as f:
    secrets = json.loads(f.read())


def get_secret(setting, section=None, secrets=secrets):
    """Get the secret variable or raise exception."""
    try:
        if section:
            return secrets[section][setting]
        return secrets[setting]
    except KeyError:
        key = setting if not section else '%s["%s"]' % (section, setting)
        error_message = 'Secrets: {} key not found in secrets.json.'.format(key)
        raise ImproperlyConfigured(error_message)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..'))
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret('SECRET_KEY')

# ALLOWED_HOSTS
VN_DOMAIN = get_secret('DOMAIN')
VN_PROTOCOL = get_secret('PROTOCOL')
VN_HTTP_DOMAIN = VN_PROTOCOL + '://' + VN_DOMAIN
ALLOWED_HOSTS = [VN_DOMAIN]

PRODUCTION_FLAG = False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django_celery_beat',

    'bitfield',
    'constance',
    'constance.backends.database',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'mptt',
    'sanitizer',
    'timezone_field',
    'snowpenguin.django.recaptcha2',

    'core.apps.CoreConfig',
    'cinfo.apps.CinfoConfig',
    'vn_core.apps.VnCoreConfig',
    'chart.apps.ChartConfig',
    'offer_service.apps.OfferServiceConfig',
    'translation.apps.TranslationConfig',
    'news.apps.NewsConfig',
    'notifications.apps.NotificationsConfig',
    'uploads.apps.UploadsConfig'
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'visual_novel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'visual_novel.context_processors.global_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'visual_novel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': get_secret(section='DATABASE', setting='HOST'),
        'PORT': get_secret(section='DATABASE', setting='PORT'),
        'NAME': get_secret(section='DATABASE', setting='NAME'),
        'USER': get_secret(section='DATABASE', setting='USER'),
        'PASSWORD': get_secret(section='DATABASE', setting='PASSWORD'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {
    'TRANSLATION_PROGRESS_POST_IN_VK_IMAGE':
        ('', 'изображение, которое прикрепляется к посту ВК о прогрессе перевода', str),
    'DEFAULT_TRANSLATION_STATUSES_TO_SHOW':
        ('active,onhold,readytogo,intest', 'список статусов перевода, которые показывать по умолчанию на странице списка переводов', str),
    'NEWS_PER_PAGE':
        (5, 'количество новостей на страницу', int),
    'CHART_POSTER_NOT_LOADED_IMAGE':
        ('', 'Изображение, которое показывать при загрузке чарта до загрузки постеров ВН', str),
    'DEFAULT_STATISTICS_MAILING_HOUR':
        (16, 'час для рассылки статистики переводов', int),
    'REDIS_CACHE_TIME_LIFE':
        (24*60*60, 'время жизни кешированных объектов в секундах', int)
}

LOGGING = {
    'version': 1.0,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s: %(levelname)s] %(message)s',
        },
    },
    'handlers': {
        'visual_novel_handler': {
            'filename': os.path.join(BASE_DIR, 'logs', 'visual_novel.log'),
            'mode': 'a+',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'simple',
            'maxBytes': 1024 * 1024 * 500,
            'backupCount': 5,
        },
        'vk_handler': {
            'filename': os.path.join(BASE_DIR, 'logs', 'vk.log'),
            'mode': 'a+',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'simple',
            'maxBytes': 1024 * 1024 * 500,
            'backupCount': 5,
        },
    },
    'loggers': {
        'vn_logger': {
            'handlers': ['visual_novel_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'vk_logger': {
            'handlers': ['vk_handler'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

MEDIA_VN_DEFAULT_FILE_DIRECTORY = 'default'
MEDIA_VN_POSTER_DIRECTORY = 'vn_poster'
MEDIA_VN_SCREENSHOTS_DIRECTORY = 'vn_screenshot'
MEDIA_VN_SCREENSHOTS_MINI_DIRECTORY = 'vn_screenshot_mini'
MEDIA_VN_NEWS = 'vn_news'
MEDIA_CUSTOM_FILES_DIRECTORY = 'custom_files'

CHART_NUMBER_OF_VN_IN_ROW = 4
POSTER_STOPPER_URL = '/media/other/file-not-found-rect.png'
STEAM_ICON_URL = '/media/other/steam-icon.png'

VNDB_API_HOST = get_secret(section='VNDB_API', setting='HOST')
VNDB_API_PORT = get_secret(section='VNDB_API', setting='PORT')
VNDB_API_PROTOCOL = get_secret(section='VNDB_API', setting='PROTOCOL')
VNDB_API_CLIENT = get_secret(section='VNDB_API', setting='CLIENT')
VNDB_API_CLIENTVER = get_secret(section='VNDB_API', setting='CLIENTVER')
VNDB_API_USERNAME = get_secret(section='VNDB_API', setting='USERNAME')
VNDB_API_PASSWORD = get_secret(section='VNDB_API', setting='PASSWORD')

DEFAULT_TIME_ZONE = 'Europe/Moscow'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

os.makedirs(os.path.join(MEDIA_ROOT, MEDIA_VN_SCREENSHOTS_MINI_DIRECTORY), exist_ok=True)

# RECAPTCHA settings
RECAPTCHA_PRIVATE_KEY = get_secret(section='CAPTCHA', setting='PRIVATE_KEY')
RECAPTCHA_PUBLIC_KEY = get_secret(section='CAPTCHA', setting='PUBLIC_KEY')

FILE_UPLOAD_MAX_MEMORY_SIZE = 200000000
FILE_UPLOAD_PERMISSIONS = 0o644

# email settings
EMAIL_HOST = get_secret(section='EMAIL_SETTINGS', setting='EMAIL_HOST')
EMAIL_PORT = get_secret(section='EMAIL_SETTINGS', setting='EMAIL_PORT')
EMAIL_HOST_USER = get_secret(section='EMAIL_SETTINGS', setting='EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_secret(section='EMAIL_SETTINGS', setting='EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = get_secret(section='EMAIL_SETTINGS', setting='EMAIL_USE_TLS')
SERVER_EMAIL = get_secret(section='EMAIL_SETTINGS', setting='SERVER_EMAIL')

# VK settings
VK_APP_ID = get_secret(section='VK', setting='APP_ID')
VK_APP_REDIRECT_URI = VN_HTTP_DOMAIN + get_secret(section='VK', setting='APP_REDIRECT_URI')
VK_APP_SECRET_KEY = get_secret(section='VK', setting='APP_SECRET_KEY')

VK_API_KEY = get_secret(section='VK', setting='API_KEY')
VK_GROUP_ID = get_secret(section='VK', setting='GROUP_ID')
VK_ADMIN_LOGIN = get_secret(section='VK', setting='ADMIN_LOGIN')

YANDEX_METRIKA_TOKEN = get_secret(section='YANDEX_METRICA_API', setting='TOKEN')
YANDEX_METRIKA_CLIENT_ID = get_secret(section='YANDEX_METRICA_API', setting='CLIENT_ID')
YANDEX_METRIKA_URL = 'https://api-metrika.yandex.ru/'

REDIS_HOST = get_secret(section='REDIS', setting='HOST')
REDIS_PORT = get_secret(section='REDIS', setting='PORT')
REDIS_CACHE_DB = get_secret(section='REDIS', setting='CACHE_DB')
REDIS_CELERY_DB = get_secret(section='REDIS', setting='CELERY_DB')

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:{}/{}".format(
            REDIS_HOST, REDIS_PORT, REDIS_CACHE_DB
        ),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

CELERY_BROKER_URL = "redis://{}:{}/{}".format(REDIS_HOST, REDIS_PORT, REDIS_CELERY_DB)
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'UTC'

CELERY_IGNORE_RESULT = False

CELERY_TASK_TIME_LIMIT = 120
CELERY_TASK_SOFT_TIME_LIMIT = 60

CELERY_TASK_QUEUES = {
    'high': Queue('high', Exchange('high', type='direct'), routing_key='high'),
    'normal': Queue('normal', Exchange('normal', type='direct'), routing_key='normal'),
    'low': Queue('low', Exchange('low', type='direct'), routing_key='low'),
}
CELERY_TASK_DEFAULT_QUEUE = 'normal'
CELERY_TASK_DEFAULT_EXCHANGE = 'normal'
CELERY_TASK_DEFAULT_ROUTING_KEY = 'normal'
CELERY_TASK_ROUTES = {}
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
