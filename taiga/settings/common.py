# -*- coding: utf-8 -*-

import os.path, sys, os
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

OUT_BASE_DIR = os.path.abspath(
    os.path.join(BASE_DIR, "..")
)

USE_X_FORWARDED_HOST = True

APPEND_SLASH = False


ADMINS = (
    ('Admin', 'example@example.com'),
)

LANGUAGES = (
    ('en', _('English')),
    ('es', _('Spanish')),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'taiga',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
SEND_BROKEN_LINK_EMAILS = True
IGNORABLE_404_ENDS = ('.php', '.cgi')
IGNORABLE_404_STARTS = ('/phpmyadmin/',)

ATOMIC_REQUESTS = True

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en'
USE_I18N = True
USE_L10N = True
LOGIN_URL='/auth/login/'
USE_TZ = True

SITES = {
    1: {"domain": "localhost:8000", "scheme": "http"},
}

SITES_FRONT = {
    1: {"domain": "localhost:9001", "scheme": "http"},
}

DOMAIN_ID = 1

# Only for django. Not used.
SITE_ID = 1

#SESSION BACKEND
SESSION_ENGINE='django.contrib.sessions.backends.db'
#SESSION_ENGINE='django.contrib.sessions.backends.cache'
#SESSION_EXPIRE_AT_BROWSER_CLOSE = False
#SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 1209600 # (2 weeks)

API_LIMIT_PER_PAGE = 0

HOST = 'http://localhost:8000'

# MAIL OPTIONS
#EMAIL_USE_TLS = False
#EMAIL_HOST = 'localhost'
#EMAIL_HOST_USER = 'user'
#EMAIL_HOST_PASSWORD = 'password'
#EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = "john@doe.com"
EMAIL_BACKEND = 'djmail.backends.default.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DJMAIL_REAL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DJMAIL_SEND_ASYNC = False
DJMAIL_MAX_RETRY_NUMBER = 3
DJMAIL_TEMPLATE_EXTENSION = 'jinja'

# Message System
#MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(OUT_BASE_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(OUT_BASE_DIR, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

DEFAULT_FILE_STORAGE = 'taiga.base.storage.FileSystemStorage'


# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Don't forget to use absolute paths, not relative paths.
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

SECRET_KEY = 'aw3+t2r(8(0kkrhg8)gx6i96v5^kv%6cfep9wxfom0%7dy0m9e'

TEMPLATE_LOADERS = [
    'django_jinja.loaders.AppLoader',
    'django_jinja.loaders.FileSystemLoader',
]

MIDDLEWARE_CLASSES = [
    'taiga.base.middleware.CoorsMiddleware',
    'taiga.base.domains.middleware.DomainsMiddleware',

    # Common middlewares
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',

    # Only needed by django admin
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.request",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
]

ROOT_URLCONF = 'taiga.urls'

TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, "templates"),
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',

    'taiga.app.TaigaMainConfig',
    'taiga.base',
    'taiga.base.users',
    'taiga.base.domains',
    'taiga.base.notifications',
    'taiga.base.searches',
    'taiga.projects',
    'taiga.projects.mixins.blocked',
    'taiga.projects.milestones',
    'taiga.projects.userstories',
    'taiga.projects.tasks',
    'taiga.projects.issues',
    'taiga.front',
    #'taiga.projects.questions',
    #'taiga.projects.documents',
    'taiga.projects.wiki',

    'reversion',
    'rest_framework',
    'djmail',
]

WSGI_APPLICATION = 'taiga.wsgi.application'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'complete': {
            'format': '%(levelname)s:%(asctime)s:%(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s:%(asctime)s: %(message)s'
        },
        'null': {
            'format': '%(message)s',
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers':['null'],
            'propagate': True,
            'level':'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'taiga': {
            'handlers': ['console'],
            'handlers': [],
            'level': 'DEBUG',
            'propagate': False,
        },
        'taiga.domains': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}


AUTH_USER_MODEL = 'users.User'
FORMAT_MODULE_PATH = 'taiga.base.formats'
DATE_INPUT_FORMATS = (
    '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%b %d %Y',
    '%b %d, %Y', '%d %b %Y', '%d %b, %Y', '%B %d %Y',
    '%B %d, %Y', '%d %B %Y', '%d %B, %Y'
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # default
)

ANONYMOUS_USER_ID = -1

GRAPPELLI_INDEX_DASHBOARD = 'taiga.dashboard.CustomIndexDashboard'

MAX_SEARCH_RESULTS = 100

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'taiga.base.auth.Token',
        'taiga.base.auth.Session',
    ),
    'FILTER_BACKEND': 'taiga.base.filters.FilterBackend',
    'EXCEPTION_HANDLER': 'taiga.base.exceptions.exception_handler',
    'PAGINATE_BY': 30,
    'MAX_PAGINATE_BY': 1000,
}


# NOTE: DON'T INSERT MORE SETTINGS AFTER THIS LINE

TEST_RUNNER="django.test.runner.DiscoverRunner"

# Test conditions
if 'test' in sys.argv:
    if "settings" not in ",".join(sys.argv):
        print ("\033[1;91mNot settings specified.\033[0m")
        print ("Try: \033[1;33mpython manage.py test --settings="
               "taiga.settings.testing -v2 taiga\033[0m")
        sys.exit(0)
