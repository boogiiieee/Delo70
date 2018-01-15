# -*- coding: utf-8 -*-

import os
def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	('GVA', 'gladkiyva@gmail.com'),
	('POA', 'poa.webaspect@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'rabota',
		'USER': 'postgres',
		'PASSWORD': '',
		'HOST': 'localhost',
		'PORT': '5432',
	}
}

TIME_ZONE = 'Asia/Novosibirsk'
LANGUAGE_CODE = 'ru'

SITE_ID = 1

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = rel('media')
STATIC_ROOT = rel('static')

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

# ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = ()

STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
	#'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 's&xgcr7dbumie@8@pyixjibt^#45o8bc$b@)onez57sr(t-q=^'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.gzip.GZipMiddleware',
	
	'django_geoip.middleware.LocationMiddleware',
	#'debug_toolbar.middleware.DebugToolbarMiddleware',
	
	'my_flatpages.middleware.FlatpageFallbackMiddleware',
	'configuration.middleware.ConfigurationMiddleware',
)

ROOT_URLCONF = 'www.urls'

WSGI_APPLICATION = 'www.wsgi.application'

TEMPLATE_DIRS = (
	rel('templates')
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',

	# django 1.2 only
	'django.contrib.messages.context_processors.messages',

	# required by django-admin-tools
	'django.core.context_processors.request',
	
	'rabota.context_processors.custom_proc',
	'geo.context_processors.custom_proc',
	'linkzilla.django.context_processors.linkzilla',
)

INSTALLED_APPS = (
	# 'admin_tools',
	# 'admin_tools.theming',
	# 'admin_tools.menu',
	# 'admin_tools.dashboard',
	
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.admin',
	'django.contrib.sitemaps',
	
	'widget_tweaks',
	'rabota',
	'feedback',
	'geo',
	'paginator',
	'registration',
	'my_flatpages',
	'configuration',
	'simpleblocks',
	'copyright',
	'ibanners',
	'news',
	
	'parsers.file_parser',
	
	'robots',
	'redactor',
	'pytils',
	'pymorphy',
	'annoying',
	'django_cleanup',
	'sorl.thumbnail',
	'debug_toolbar',
	'captcha',
	'complaint',
	#'south',
	'django_geoip',
	'linkzilla.django',
)

REDACTOR_OPTIONS = {'lang':'ru', 'tidyHtml':False}

CACHE_TABLE = 'cache_table'
CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
		'LOCATION': CACHE_TABLE,
		# 'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
	}
}

ROBOTS_SITEMAP_URLS = ['http://delo70.ru/sitemap.xml']
ROBOTS_SITEMAP_HOST = 'delo70.ru'

LINKZILLA_SERVICES = ['sape']
LINKZILLA_CONFIG = {
	'sape': {
		'name': 'sape',
		'user': '85aebdc2f11eecf7da7003c7a3e88ed1',
		'host': 'delo70.ru',
		'storage': {
			'name': 'dbm',
			'database_path': rel('linkzilla'),
		},
	},
}

PAGINATE_BY = 20

LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_ACTIVATION_DAYS = 2

ADMIN_TOOLS_THEMING_CSS = 'admin_tools/css/theming_webaspect.css'
ADMIN_TOOLS_INDEX_DASHBOARD = 'www.dashboard.CustomIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'www.dashboard.CustomAppIndexDashboard'

PYMORPHY_DICTS = {
	'ru': { 'dir': os.path.join(MEDIA_ROOT, 'morphy_ru') },
}

DEFAULT_FROM_EMAIL = 'tester@web-aspect.ru'
EMAIL_HOST = 'smtp.locum.ru'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'tester@web-aspect.ru'
EMAIL_HOST_PASSWORD = 'iostream'
EMAIL_USE_TLS = False

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_PANELS = (
	'debug_toolbar.panels.version.VersionDebugPanel',
	'debug_toolbar.panels.timer.TimerDebugPanel',
	'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
	'debug_toolbar.panels.headers.HeaderDebugPanel',
	'debug_toolbar.panels.profiling.ProfilingDebugPanel',
	'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
	'debug_toolbar.panels.sql.SQLDebugPanel',
	'debug_toolbar.panels.template.TemplateDebugPanel',
	'debug_toolbar.panels.cache.CacheDebugPanel',
	'debug_toolbar.panels.signals.SignalDebugPanel',
	'debug_toolbar.panels.logger.LoggingPanel',
)

DEBUG_TOOLBAR_CONFIG = {
	'INTERCEPT_REDIRECTS': False,
}

GEOIP_LOCATION_MODEL = 'geo.models.CustomLocation'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
		'linkexchange': {
            'handlers': ['mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
