"""Settings."""

import ipaddress
import os

from django.contrib.messages import constants as message_constants

import dj_database_url
import django_feature_policy
import sentry_sdk
from sentry_sdk.integrations import celery as sentry_celery
from sentry_sdk.integrations import django as sentry_django

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get("SECRET_KEY", "not-so-secret")
DEBUG = bool(os.environ.get("DEBUG"))


# Allowed Hosts
# https://docs.djangoproject.com/en/stable/ref/settings/#allowed-hosts

ALLOWED_HOSTS = []

if "CANONICAL_HOST" in os.environ:
    canonical_host = os.environ["CANONICAL_HOST"]
    ALLOWED_HOSTS.append(canonical_host)
    if canonical_host.startswith("www."):
        ALLOWED_HOSTS.append(canonical_host[4:])
    else:
        ALLOWED_HOSTS.append(f"www.{canonical_host}")

if "HEROKU_APP_NAME" in os.environ:
    ALLOWED_HOSTS.append(f"{os.environ['HEROKU_APP_NAME']}.herokuapp.com")

# ALLOWED_HOSTS cannot pass Django's system check when empty.
# We set a placeholder value here so we can successfully deploy the app to Heroku before dyno
# metadata is enabled.
if not ALLOWED_HOSTS and not DEBUG:
    ALLOWED_HOSTS.append("127.0.0.1")


# Enforce host
# https://github.com/dabapps/django-enforce-host

ENFORCE_HOST = os.environ.get("CANONICAL_HOST")


# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    # Required ordering (https://github.com/adamcharnock/django-su)
    "django_su",
    "django.contrib.admin",
    # Third-party
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "ckeditor",
    "crispy_forms",
    "debug_toolbar",
    "django_countries",
    "django_tables2",
    "djcelery_email",
    "flatblocks",
    "tz_detect",
    # First-party
    "af_gang_mail",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_feature_policy.FeaturePolicyMiddleware",
    "csp.middleware.CSPMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "tz_detect.middleware.TimezoneMiddleware",
]

ROOT_URLCONF = "af_gang_mail.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            # workaround for https://github.com/pennersr/django-allauth/issues/370
            "af_gang_mail/templates"
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "af_gang_mail.context_processors.edit_mode",
                "af_gang_mail.context_processors.google",
                "af_gang_mail.context_processors.sentry",
            ],
        },
    },
]

WSGI_APPLICATION = "af_gang_mail.wsgi.application"


# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases

DATABASES = {"default": dj_database_url.config(conn_max_age=600)}


# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/
# http://whitenoise.evans.io/en/stable/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Internal IPs (required for Django Debug Toolbar)
# https://docs.djangoproject.com/en/stable/ref/settings/#internal-ips


class IPv4List(list):
    """IPv4 addresses from CIDR."""

    def __init__(self, cidr):
        super().__init__()
        self.network = ipaddress.IPv4Network(cidr)

    def __contains__(self, ip):
        return ipaddress.IPv4Address(ip) in self.network


INTERNAL_IPS = IPv4List(os.environ.get("INTERNAL_IP_CIDR", "127.0.0.1/32"))


# Django Debug Toolbar
# https://django-debug-toolbar.readthedocs.io/en/stable/configuration.html

DEBUG_TOOLBAR_CONFIG = {"SHOW_COLLAPSED": True}


# Sentry
# https://sentry.io/data-power/data-power/getting-started/python-django/


SENTRY_DSN = os.environ.get("SENTRY_DSN")
SENTRY_ENVIRONMENT = os.environ.get(
    "SENTRY_ENVIRONMENT", os.environ.get("HEROKU_APP_NAME")
)
SENTRY_RELEASE = os.environ.get("SENTRY_RELEASE", os.environ.get("HEROKU_SLUG_COMMIT"))

sentry_sdk.init(
    integrations=[
        sentry_celery.CeleryIntegration(),
        sentry_django.DjangoIntegration(),
    ],
    environment=SENTRY_ENVIRONMENT,
    release=SENTRY_RELEASE,
)


# Security
# https://docs.djangoproject.com/en/stable/topics/security/

SECURE_HSTS_SECONDS = 0 if DEBUG else 2592000  # 30 days (60 * 60 * 24 * 30)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"


# Content Security Policy
# https://django-csp.readthedocs.io/en/stable/configuration.html

CSP_DEFAULT_SRC = []
CSP_IMG_SRC = [
    "'self'",
    "https://maps.gstatic.com/mapfiles/api-3/images/",
    "https://*.usefathom.com",
]
CSP_CONNECT_SRC = ["'self'", "https://*.ingest.sentry.io", "https://*.usefathom.com"]
CSP_STYLE_SRC = [
    "'self'",
    "'unsafe-inline'",  # required for Google places auto suggest
]
CSP_SCRIPT_SRC = [
    "'self'",
    "'unsafe-inline'",  # required for Google places auto suggest
    "https://maps.googleapis.com",
    "https://cdn.usefathom.com",
]
CSP_FONT_SRC = ["'self'"]
CSP_INCLUDE_NONCE_IN = ["script-src"]
CSP_REPORT_URI = os.environ.get("CSP_REPORT_URI", None)


# Feature policy
# https://github.com/adamchainz/django-feature-policy#setting

FEATURE_POLICY = {
    feature_name: "none" for feature_name in django_feature_policy.FEATURE_NAMES
}


# Sites
# https://docs.djangoproject.com/en/3.0/ref/contrib/sites/

SITE_ID = 1


# Authentication
# https://docs.djangoproject.com/en/stable/topics/auth/customizing/
# https://django-allauth.readthedocs.io/

AUTH_USER_MODEL = "af_gang_mail.User"
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    "django_su.backends.SuBackend",
]
LOGIN_REDIRECT_URL = "home"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_FORMS = {
    "login": "af_gang_mail.forms.LoginForm",
    "reset_password": "af_gang_mail.forms.ResetPasswordForm",
    "signup": "af_gang_mail.forms.SignupForm",
}


# Cast user to string to get display name.
ACCOUNT_USER_DISPLAY = str  # pylint: disable=invalid-name


# Celery
# https://docs.celeryproject.org/en/stable/userguide/configuration.html
# https://www.cloudamqp.com/docs/celery.html

CELERY_BROKER_CONNECTION_TIMEOUT = int(
    os.environ.get("CELERY_BROKER_CONNECTION_TIMEOUT", 30)
)
CELERY_BROKER_HEARTBEAT = None
CELERY_BROKER_POOL_LIMIT = int(os.environ.get("CELERY_BROKER_POOL_LIMIT", 1))
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", os.environ.get("CLOUDAMQP_URL"))
CELERY_EVENT_QUEUE_EXPIRES = int(os.environ.get("CELERY_EVENT_QUEUE_EXPIRES", 60))
CELERY_RESULT_BACKEND = None
CELERY_TASK_ALWAYS_EAGER = bool(os.environ.get("CELERY_TASK_ALWAYS_EAGER", False))
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_TASK_SOFT_TIME_LIMIT = int(os.environ.get("CELERY_TASK_SOFT_TIME_LIMIT", 30))
CELERY_TASK_TIME_LIMIT = int(os.environ.get("CELERY_TASK_TIME_LIMIT", 60))
CELERY_WORKER_CONCURRENCY = int(os.environ.get("CELERY_WORKER_CONCURRENCY", 5))
CELERY_WORKER_PREFETCH_MULTIPLIER = int(
    os.environ.get("CELERY_WORKER_PREFETCH_MULTIPLIER", 1)
)
CELERY_WORKER_SEND_TASK_EVENTS = bool(os.environ.get("CELERY_WORKER_SEND_TASK_EVENTS"))


# Email
# https://docs.djangoproject.com/en/stable/topics/email/
# https://github.com/pmclanahan/django-celery-email
# https://anymail.readthedocs.io/en/stable/installation/#anymail-settings-reference

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "noreply@mail.afgang.co.uk")
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"

if "SENDINBLUE_API_KEY" in os.environ:
    CELERY_EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"
    ANYMAIL = {"SENDINBLUE_API_KEY": os.environ["SENDINBLUE_API_KEY"]}

else:
    CELERY_EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.environ.get("SMTP_SERVER")
    EMAIL_PORT = int(os.environ.get("SMTP_PORT", 587))
    EMAIL_HOST_USER = os.environ.get("SMTP_USERNAME")
    EMAIL_HOST_PASSWORD = os.environ.get("SMTP_PASSWORD")
    EMAIL_USE_TLS = bool(os.environ.get("SMTP_TLS", True))


# Google APIs

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")


# Logging
# https://docs.djangoproject.com/en/stable/topics/logging/

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler",},},
    "root": {"handlers": ["console"], "level": "INFO",},
}


# Messages
# https://docs.djangoproject.com/en/3.0/ref/contrib/messages/

MESSAGE_LEVEL = message_constants.DEBUG if DEBUG else message_constants.INFO


# Flat Blocks

FLATBLOCKS_AUTOCREATE_STATIC_BLOCKS = True


# django-ckeditor
# https://github.com/django-ckeditor/django-ckeditor#installation

CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_CONFIGS = {
    "default": {
        "height": 300,
        "width": 600,
        "toolbar": "af_gang_mail",
        "toolbar_af_gang_mail": [
            ["Bold", "Italic"],
            ["NumberedList", "BulletedList"],
            ["Link", "Unlink"],
            ["RemoveFormat", "Source"],
        ],
    },
}


# django-tz-detect
# https://github.com/adamcharnock/django-tz-detect

TZ_DETECT_COUNTRIES = ["GB", "US"]


# Draw creation

CREATE_DRAW_MAX_ATTEMPTS = int(os.environ.get("CREATE_DRAW_MAX_ATTEMPTS", 100))

# Default value based on Heroku hobby dynos. On my laptop this was 0.001.
CREATE_DRAW_SECONDS_PER_USER = float(
    os.environ.get("CREATE_DRAW_SECONDS_PER_USER", 0.003)
)
