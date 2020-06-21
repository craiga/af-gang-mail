"""Settings."""

import ipaddress
import os

import dj_database_url
import django_feature_policy
import sentry_sdk
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
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
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
]

ROOT_URLCONF = "af_gang_mail.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
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

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


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


# Whitenoise
# http://whitenoise.evans.io/en/stable/

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Sentry
# https://sentry.io/data-power/data-power/getting-started/python-django/


SENTRY_DSN = os.environ.get("SENTRY_DSN")
SENTRY_ENVIRONMENT = os.environ.get(
    "SENTRY_ENVIRONMENT", os.environ.get("HEROKU_APP_NAME")
)
SENTRY_RELEASE = os.environ.get("SENTRY_RELEASE", os.environ.get("HEROKU_SLUG_COMMIT"))

sentry_sdk.init(
    integrations=[sentry_django.DjangoIntegration()],
    environment=SENTRY_ENVIRONMENT,
    release=SENTRY_RELEASE,
)


# Content Security Policy
# https://django-csp.readthedocs.io/en/stable/configuration.html

CSP_DEFAULT_SRC = []
CSP_IMG_SRC = ["'self'", "https://secure.gravatar.com/avatar/"]
CSP_CONNECT_SRC = ["'self'", "https://*.ingest.sentry.io"]
CSP_STYLE_SRC = ["'self'"]
CSP_SCRIPT_SRC = ["'self'"]
CSP_INCLUDE_NONCE_IN = ["script-src"]
CSP_REPORT_URI = os.environ.get("CSP_REPORT_URI", None)


# Feature policy
# https://github.com/adamchainz/django-feature-policy#setting

FEATURE_POLICY = {
    feature_name: "none" for feature_name in django_feature_policy.FEATURE_NAMES
}


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
CSP_IMG_SRC = ["'self'"]
CSP_CONNECT_SRC = ["'self'", "https://*.ingest.sentry.io"]
CSP_STYLE_SRC = ["'self'"]
CSP_SCRIPT_SRC = ["'self'"]
CSP_INCLUDE_NONCE_IN = ["script-src"]
CSP_REPORT_URI = os.environ.get("CSP_REPORT_URI", None)


# Feature policy
# https://github.com/adamchainz/django-feature-policy#setting

FEATURE_POLICY = {
    feature_name: "none" for feature_name in django_feature_policy.FEATURE_NAMES
}
