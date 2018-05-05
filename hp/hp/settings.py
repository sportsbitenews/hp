"""
Django settings for hp project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import ipaddress
import os
from datetime import timedelta

from celery.schedules import crontab

from django.contrib.messages import constants as messages
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from core.constants import ACTIVITY_FAILED_LOGIN
from core.constants import ACTIVITY_REGISTER
from core.constants import ACTIVITY_RESET_PASSWORD

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ENABLE_DEBUG_TOOLBAR = None

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = None
_DEFAULT_INSTALLED_APPS = [
    'core',
    'antispam',
    'blog',  # blog posts and pages
    'bootstrap',  # bootstrap enhancements
    'account',  # account management
    'feed',  # RSS/Atom feeds
    'certs',  # log certificates
    'stats',  # Statistics gathering
    'conversejs',  # webchat

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',

    'captcha',
    'django_object_actions',  # object actions
    'mptt',  # Tree structure for MenuItem
    'reversion',  # object history for blogposts/pages
    'tinymce',  # Rich text editor
    'xmpp_http_upload',  # XEP-0363
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.HomepageMiddleware',
]

ROOT_URLCONF = 'hp.urls'

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
                'core.context_processors.basic',
                'blog.context_processors.global_pages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'
LANGUAGES = [
    ('de', _('German')),
    ('en', _('English')),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
AUTH_USER_MODEL = 'account.User'
LOGIN_URL = reverse_lazy('account:login')
LOGIN_REDIRECT_URL = reverse_lazy('account:detail')

# Authenticate against the XMPP server
AUTHENTICATION_BACKENDS = [
    'xmpp_backends.django.auth_backends.XmppBackendBackend',
]

JS_FILES = None
_DEFAULT_JS_FILES = [
    'lib/jquery/jquery.js',
    'lib/prism/prism.js',
    'lib/popper.js',
    'lib/bootstrap/js/bootstrap.js',
    'core/js/base.js',
    'core/js/captcha.js',
    'bootstrap/js/bootstrap.js',
    'account/js/gpgmixin.js',
    'account/js/email_verified_domain_widget.js',
    'account/js/username_widget.js',
    'account/js/base.js',
    'account/js/notifications.js',
    'certs/certificate.js',
]
CSS_FILES = None
_DEFAULT_CSS_FILES = [
    'lib/bootstrap/css/bootstrap.min.css',
    'lib/prism/prism.css',
    'lib/fontawesome/web-fonts-with-css/css/fontawesome-all.css',
    'core/css/bootstrap-hp.css',
    'core/css/base.css',
    'core/css/clients.css',
    'core/css/captcha.css',
    'bootstrap/css/bootstrap.css',
    'account/css/base.css',
    'account/css/email_verified_domain_widget.css',
    'account/css/gpgmixin.css',
    'account/css/notifications.css',
    'account/css/username_widget.css',
    'blog/blog.css',
    'certs/certificate.css',
]

############
# TinyMCE4 #
############
TINYMCE_JS_URL = 'lib/tinymce/js/tinymce/tinymce.min.js'
TINYMCE_DEFAULT_CONFIG = {
    'selector': 'textarea',
    'theme': 'modern',
    'setup': 'tinymce_setup',
    'browser_spellcheck': True,
    'convert_urls': False,
    'plugins': 'link image lists preview table code codesample',
    'toolbar1': 'styleselect | bold italic underline strikethrough '
                '| alignleft aligncenter alignright alignjustify '
                '| bullist numlist | outdent indent | link image ',
    'toolbar2': 'badges tooltips icons | table codesample '
                '| code removeformat',
    'contextmenu': 'formats | link image',
    'menubar': False,
    'inline': False,
    'extended_valid_elements': 'span[class]',  # required for fontawesome
    'style_formats': [
        {'title': 'Headers', 'items': [
            # NOTE: <h1> is already the page title, so actual h-level is one level down from tite
            {'title': 'Header 1', 'block': 'h2', },
            {'title': 'Header 2', 'block': 'h3', },
            {'title': 'Header 3', 'block': 'h4', },
        ], },
        {'title': 'Alerts', 'items': [
            {'title': 'Success', 'block': 'div', 'classes': 'alert alert-success', },
            {'title': 'Info', 'block': 'div', 'classes': 'alert alert-info', },
            {'title': 'Warning', 'block': 'div', 'classes': 'alert alert-warning', },
            {'title': 'Danger', 'block': 'div', 'classes': 'alert alert-danger', },
        ], },
        {'title': 'Context', 'items': [
            {'title': 'textmuted', 'inline': 'span', 'classes': 'text-muted', },
            {'title': 'textprimary', 'inline': 'span', 'classes': 'text-primary', },
            {'title': 'textsuccess', 'inline': 'span', 'classes': 'text-success', },
            {'title': 'textinfo', 'inline': 'span', 'classes': 'text-info', },
            {'title': 'textwarning', 'inline': 'span', 'classes': 'text-warning', },
            {'title': 'textdanger', 'inline': 'span', 'classes': 'text-danger', },
        ], },
        {'title': 'OS-specific', 'items': [
            {'title': 'Android', 'selector': 'p,h1,h2,h3,h4,h5,h6,tr,td,th,div,ul,ol,li,table,img',
             'classes': 'os-android', },
            {'title': 'Browser', 'selector': 'p,h1,h2,h3,h4,h5,h6,tr,td,th,div,ul,ol,li,table,img',
             'classes': 'os-browser', },
            {'title': 'iOS (iPhone/...)', 'selector': 'p,h1,h2,h3,h4,h5,h6,tr,td,th,div,ul,ol,li,table,img',
             'classes': 'os-ios', },
            {'title': 'Linux', 'selector': 'p,h1,h2,h3,h4,h5,h6,tr,td,th,div,ul,ol,li,table,img',
             'classes': 'os-linux', },
            {'title': 'Linux (console)', 'selector': 'p,h1,h2,h3,h4,h5,h6,tr,td,th,div,ul,ol,li,table,img',
             'classes': 'os-console', },
            {'title': 'MacOS X', 'selector': 'p,h1,h2,h3,h4,h5,h6,tr,td,th,div,ul,ol,li,table,img',
             'classes': 'os-osx', },
            {'title': 'Windows', 'selector': 'p,h1,h2,h3,h4,h5,h6,tr,td,th,div,ul,ol,li,table,img',
             'classes': 'os-win', },
        ], },
    ],
    'formats': {
        'underline': {'inline': 'u', 'exact': True},
        'strikethrough': {'inline': 's', 'exact': True},
        #'inlinecode': {'inline': 'code', 'exact': True},

        'alignleft': {'selector': 'p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li,table,img',
                      'classes': 'text-left', },
        'aligncenter': {'selector': 'p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li,table,img',
                        'classes': 'text-center', },
        'alignright': {'selector': 'p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li,table,img',
                       'classes': 'test-right', },
        'alignjustify': {'selector': 'p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li,table,img',
                         'classes': 'text-justify', },

        'badge_primary': {'inline': 'span', 'classes': 'badge badge-primary', },
        'badge_secondary': {'inline': 'span', 'classes': 'badge badge-secondary', },
        'badge_success': {'inline': 'span', 'classes': 'badge badge-success', },
        'badge_info': {'inline': 'span', 'classes': 'badge badge-info', },
        'badge_warning': {'inline': 'span', 'classes': 'badge badge-warning', },
        'badge_danger': {'inline': 'span', 'classes': 'badge badge-danger', },

        'tablestriped': {'selector': 'table', 'classes': 'table-striped'},
        'tablebordered': {'selector': 'table', 'classes': 'table-bordered'},
        'tablehover': {'selector': 'table', 'classes': 'table-hover'},
        'tablecondensed': {'selector': 'table', 'classes': 'table-condensed'},
        'tableresponsive': {'selector': 'table', 'wrapper': True, 'exact': True, 'remove': 'all',
                            'block': 'div', 'classes': 'table-responsive-test'},
    },
    'content_css': [
        '/static/lib/bootstrap/css/bootstrap.min.css',
        '/static/lib/fontawesome/web-fonts-with-css/css/fontawesome-all.min.css',
        '/static/core/css/base.css',
        '/static/core/css/tinymce-preview.css',
    ],
    # Do table styling with bootstrap classes
    'table_toolbar': "tableprops tabledelete "
                     "| tablestriped tablebordered tablehover tablecondensed tableresponsive "
                     "| tableinsertrowbefore tableinsertrowafter tabledeleterow "
                     "| tableinsertcolbefore tableinsertcolafter tabledeletecol",
    'table_default_attributes': {
        'class': 'table',
    },
    'table_appearance_options': False,
    'table_advtab': False,
    'table_cell_advtab': False,
    'table_row_advtab': False,
    'table_row_class_list': [
        {'title': 'None', 'value': ''},
        {'title': 'Active', 'value': 'active'},
        {'title': 'Success', 'value': 'success'},
        {'title': 'Info', 'value': 'info'},
        {'title': 'Warning', 'value': 'warning'},
        {'title': 'Danger', 'value': 'danger'},
    ],
    'table_cell_class_list': [
        {'title': 'None', 'value': ''},
        {'title': 'Active', 'value': 'active'},
        {'title': 'Success', 'value': 'success'},
        {'title': 'Info', 'value': 'info'},
        {'title': 'Warning', 'value': 'warning'},
        {'title': 'Danger', 'value': 'danger'},
    ],
    # Displays the current HTML tree (e.g. "p > strong > ...") at the bottom
    #'statusbar': False,
    'height': 300,

    # codesample
    'codesample_languages': [
        {'text': 'Apache', 'value': 'apacheconf', },
        {'text': 'Bash', 'value': 'bash', },
        {'text': 'C', 'value': 'c', },
        {'text': 'CSS', 'value': 'css', },
        {'text': 'Diff', 'value': 'diff', },
        {'text': 'Django', 'value': 'django', },
        {'text': 'HTML/XML', 'value': 'markup', },
        {'text': 'JSON', 'value': 'json', },
        {'text': 'JavaScript', 'value': 'javascript', },
        {'text': 'PHP', 'value': 'php', },
        {'text': 'Python', 'value': 'python', },
    ],
    'noneditable_noneditable_class': 'fa',
}

###################
# CUSTOM SETTINGS #
###################

# used in hp.urls
ADDITIONAL_URL_PATHS = []

# Override message tags to match bootstrap alert classes.
#       See: https://docs.djangoproject.com/en/1.10/ref/contrib/messages/#message-tags
# The second class is the django default, needed in django admin.
MESSAGE_TAGS = {
    messages.ERROR: 'danger error',
    messages.DEBUG: 'info debug',
}
ACCOUNT_EXPIRES_DAYS = None
ACCOUNT_EXPIRES_NOTIFICATION_DAYS = None

ADMIN_URL = '/admin/'

# Custom media root directory for Images uploaded via admin
BLOG_MEDIA_ROOT = None
BLOG_MEDIA_URL = None

# pages
CLIENTS_PAGE = None
FAQ_PAGE = None

XMPP_HOSTS = {}
CONTACT_ADDRESS = None
CONTACT_MUC = None
DEFAULT_XMPP_HOST = None
DEFAULT_FROM_EMAIL = None

# How long confirmation emails remain valid
USER_CONFIRMATION_TIMEOUT = timedelta(hours=48)

LOG_FORMAT = '[%(asctime).19s %(levelname)-8s] %(message)s'  # .19s = only first 19 chars
LIBRARY_LOG_LEVEL = 'WARN'
LOG_LEVEL = 'INFO'
COPYRIGHT_NOTICE = _('© 2010-%(year)s, %(brand)s.')

FACEBOOK_PAGE = ''
TWITTER_HANDLE = ''

_DEFAULT_SOCIAL_MEDIA_TEXTS = {
    'account:register': {
        'meta_desc': _('Register for an account at jabber.at, jabber.zone or xmpp.zone. Its fast, '
                       'free, easy and safe!'),
        'title': _('Register at %(BRAND)s'),
        'twitter_desc': _('Register now for an account at jabber.at, jabber.zone or xmpp.zone. '
                          'It\'s fast, free, easy and safe!'),
        'og_desc': _('Jabber is a free and open instant messaging network. Register now for an '
                     'account at jabber.at, jabber.zone or xmpp.zone. It\'s fast, free, easy and '
                     'safe!'),
    },
    'blog:home': {
        'meta_desc': _('A free, stable, secure and feature-rich Jabber/XMPP server. '
                       'Join the free and open Jabber instant messaging network today!'),
        'twitter_title': _('A free and secure Jabber/XMPP server'),
        'og_title': _('A free, secure, feature-rich Jabber/XMPP server'),
    },
    'core:contact': {
        'meta_desc': _('Contact us here if you cannot connect or have issues with our service '
                       'best solved privately.'),
        'og_desc': _('Contact us here if you cannot connect or have issues with our service '
                     'best solved privately. We will reply via email as soon as possible. '
                     'You can also contact us via chatroom, Twitter or Facebook.'),
        'title': _('Contact %(BRAND)s support'),
    },
}
SOCIAL_MEDIA_TEXTS = {}

LINK_TARGET_MODELS = ['blog.page', 'blog.blogpost']
ACCOUNT_USER_MENU = None
_DEFAULT_ACCOUNT_USER_MENU = [
    ('account:detail', {
        'title': _('Overview'),
        'requires_confirmation': False,
    }),
    ('account:sessions', {
        'title': _('Current sessions'),
    }),
    ('account:notifications', {
        'title': _('Notifications'),
    }),
    ('account:set_password', {
        'title': _('Set password'),
    }),
    ('account:set_email', {
        'title': _('Set E-Mail'),
        'requires_confirmation': False,
    }),
    ('account:xep0363', {
        'title': _('HTTP uploads'),
    }),
    ('account:gpg', {
        'title': _('GPG keys'),
    }),
    ('account:log', {
        'title': _('Recent activity'),
        'requires_confirmation': False,
    }),
    ('account:delete', {
        'title': _('Delete account'),
    }),
]

OBSERVATORY_URL = 'https://check.messaging.one/badge.php'

SIDEBAR_PANELS = None
_DEFAULT_SIDEBAR_PANELS = [
    'core/cards/languages.html',
    'core/cards/updates.html',
]

################
# GPG settings #
################
GPG_KEYSERVER = 'http://pool.sks-keyservers.net:11371'

# Default GPG backend configuration
GPG_BACKENDS = {
    'default': {
        'BACKEND': 'gpgliblib.gpgme.GpgMeBackend',
        'HOME': os.path.join(ROOT_DIR, 'gnupg'),
        # Optional settings:
        #'PATH': '/home/...',  # Path to 'gpg' binary
        #'ALWAYS_TRUST': True,   # Ignore trust in all operations
        #'OPTIONS': {...},  # Any custom options for the specific backend implementation
    },
}

# Directory where public/private keys are stored for signing.
GPG_KEYDIR = os.path.join(BASE_DIR, 'gpg-keys')
MAX_UPLOAD_SIZE = 1024 * 1024 * 2

###################
# Celery settings #
###################
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_SEND_TASK_ERROR_EMAILS = True

# Periodic tasks
CELERY_BEAT_SCHEDULE = {
    'core cleanup': {
        'task': 'core.tasks.cleanup',
        'schedule': crontab(hour=3, minute=0),
    },
    'account cleanup': {
        'task': 'account.tasks.cleanup',
        'schedule': crontab(hour=3, minute=5),
    },
    'account last activity': {
        'task': 'account.tasks.update_last_activity',
        'schedule': crontab(minute=12),
    },
    'download_xmpp_net_badges': {
        'task': 'blog.tasks.download_xmpp_net_badges',
        'schedule': crontab(hour=9, minute=35),
    },
}
CELERY_WORKER_LOG_FORMAT = None
CELERY_WORKER_TASK_LOG_FORMAT = None

######################
# Anti-Spam settings #
######################

# Captchas
ENABLE_CAPTCHAS = True
CAPTCHA_LENGTH = 8
CAPTCHA_FONT_SIZE = 32
CAPTCHA_TEXT_FIELD_TEMPLATE = 'core/captcha/text_field.html'

# DNSBL lists
DNSBL = (
    'sbl.spamhaus.org',
    'xbl.spamhaus.org',
    'proxies.dnsbl.sorbs.net',
    'spam.abuse.ch',
    'cbl.abuseat.org',
)

# Ratelimit
RATELIMIT_CONFIG = {
    ACTIVITY_REGISTER: (
        (timedelta(hours=1), 3, ),
        (timedelta(days=1), 5, ),
    ),
    ACTIVITY_FAILED_LOGIN: (
        (timedelta(minutes=30), 3, ),
    ),
    ACTIVITY_RESET_PASSWORD: (
        (timedelta(minutes=30), 3, ),
    ),
}
SPAM_BLACKLIST = set()
BLOCKED_EMAIL_TIMEOUT = None
BLOCKED_IPADDRESS_TIMEOUT = timedelta(days=31)

# Email addresses using these domains cannot be used for registration
BANNED_EMAIL_DOMAINS = set()
EMAIL_BLACKLIST = tuple()
EMAIL_WHITELIST = tuple()

MIN_USERNAME_LENGTH = 2
MAX_USERNAME_LENGTH = 64
REQUIRE_UNIQUE_EMAIL = False

####################
# Privacy settings #
####################
USER_LOGENTRY_EXPIRES = timedelta(days=31)

###########
# WebChat #
###########
CONVERSEJS_CONFIG = {}
CONVERSEJS_SETUP_CALLBACK = None

try:
    from .localsettings import *  # NOQA
except ImportError:
    pass

if ENABLE_DEBUG_TOOLBAR is None:
    ENABLE_DEBUG_TOOLBAR = DEBUG

if ENABLE_DEBUG_TOOLBAR is True:
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    _DEFAULT_INSTALLED_APPS.append('debug_toolbar')
    INTERNAL_IPS = ['127.0.0.1']

# Make sure some required settings are set
if not XMPP_HOSTS:
    raise ImproperlyConfigured("The XMPP_HOSTS setting is undefined.")
if not DEFAULT_XMPP_HOST:
    raise ImproperlyConfigured("The DEFAULT_XMPP_HOST setting is undefined.")
elif DEFAULT_XMPP_HOST not in XMPP_HOSTS:
    raise ImproperlyConfigured("Host named by DEFAULT_XMPP_HOST is not defined in XMPP_HOSTS.")
if not DEFAULT_FROM_EMAIL:
    raise ImproperlyConfigured("The DEFAULT_FROM_EMAIL setting is undefined.")

if CELERY_WORKER_LOG_FORMAT is None:
    CELERY_WORKER_LOG_FORMAT = LOG_FORMAT
if CELERY_WORKER_TASK_LOG_FORMAT is None:
    # The default includes the task_name
    CELERY_WORKER_TASK_LOG_FORMAT = '[%(asctime).19s %(levelname)-8s] [%(task_name)s] %(message)s'

if INSTALLED_APPS is None:
    INSTALLED_APPS = _DEFAULT_INSTALLED_APPS
elif callable(INSTALLED_APPS):
    INSTALLED_APPS = INSTALLED_APPS(_DEFAULT_INSTALLED_APPS)

# If ACCOUNT_USER_MENU is None, set the default value, if it's a callable, pass default to it
if ACCOUNT_USER_MENU is None:
    ACCOUNT_USER_MENU = _DEFAULT_ACCOUNT_USER_MENU
elif callable(ACCOUNT_USER_MENU):
    ACCOUNT_USER_MENU = ACCOUNT_USER_MENU(_DEFAULT_ACCOUNT_USER_MENU)

if JS_FILES is None:
    JS_FILES = _DEFAULT_JS_FILES
elif callable(JS_FILES):
    JS_FILES = JS_FILES(_DEFAULT_JS_FILES)

if CSS_FILES is None:
    CSS_FILES = _DEFAULT_CSS_FILES
elif callable(CSS_FILES):
    CSS_FILES = CSS_FILES(_DEFAULT_CSS_FILES)

if SIDEBAR_PANELS is None:
    SIDEBAR_PANELS = _DEFAULT_SIDEBAR_PANELS
elif callable(SIDEBAR_PANELS):
    SIDEBAR_PANELS = SIDEBAR_PANELS(_DEFAULT_SIDEBAR_PANELS)

if ACCOUNT_EXPIRES_DAYS is not None:
    if ACCOUNT_EXPIRES_NOTIFICATION_DAYS is None:
        ACCOUNT_EXPIRES_NOTIFICATION_DAYS = ACCOUNT_EXPIRES_DAYS - 7

    ACCOUNT_EXPIRES_DAYS = timedelta(days=ACCOUNT_EXPIRES_DAYS)
    ACCOUNT_EXPIRES_NOTIFICATION_DAYS = timedelta(days=ACCOUNT_EXPIRES_NOTIFICATION_DAYS)

SPAM_BLACKLIST = set([ipaddress.ip_network(addr) for addr in SPAM_BLACKLIST])

# set social media text defaults
for key, value in _DEFAULT_SOCIAL_MEDIA_TEXTS.items():
    if key in SOCIAL_MEDIA_TEXTS:
        SOCIAL_MEDIA_TEXTS[key].update(value)
    else:
        SOCIAL_MEDIA_TEXTS[key] = value

    # set empty values by default, otherwise we might get VariableLookup issues
    SOCIAL_MEDIA_TEXTS[key].setdefault('title', '')
    SOCIAL_MEDIA_TEXTS[key].setdefault('meta_desc', '')

# Make sure GPG home directories exist
for backend, config in GPG_BACKENDS.items():
    if config.get('HOME') and not os.path.exists(config['HOME']):
        os.makedirs(config['HOME'])
if not os.path.exists(GPG_KEYDIR):
    os.makedirs(GPG_KEYDIR)

# set some defaults for XMPP_HOSTS
for key, config in XMPP_HOSTS.items():
    config['NAME'] = key
    config.setdefault('ALLOWED_HOSTS', [])
    config.setdefault('ALLOW_EMAIL', False)
    config.setdefault('BRAND', key)
    config.setdefault('CANONICAL_BASE_URL', 'https://%s' % key)
    config.setdefault('CONTACT_ADDRESS', CONTACT_ADDRESS)
    config.setdefault('DEFAULT_FROM_EMAIL', DEFAULT_FROM_EMAIL)
    config.setdefault('REGISTRATION', True)

if not ALLOWED_HOSTS:
    for config in XMPP_HOSTS.values():
        ALLOWED_HOSTS += XMPP_HOSTS.get('ALLOWED_HOSTS', [])


# Hosts managed by this homepage
MANAGED_HOSTS = {k: v for k, v in XMPP_HOSTS.items() if v.get('MANAGE', True)}
# Hosts where registration is possible via this homepage
REGISTER_HOSTS = {k: v for k, v in MANAGED_HOSTS.items() if v.get('REGISTRATION', True)}

CONVERSEJS_CONFIG.setdefault('locales_url',
                             '/static/conversejs/locale/{{{locale}}}/LC_MESSAGES/converse.json')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'simple': {
            'format': LOG_FORMAT,
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'requests': {'level': LIBRARY_LOG_LEVEL, },

        'account': {'level': LOG_LEVEL, },
        'bootstrap': {'level': LOG_LEVEL, },
        'core': {'level': LOG_LEVEL, },
        'gpgliblib': {'level': LOG_LEVEL, },
    },
    'root': {
        'handlers': ['console', ],
        'level': LIBRARY_LOG_LEVEL,
    },
}
