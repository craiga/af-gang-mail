"""Context processors."""

from django.conf import settings


def sentry(request):
    return {
        "sentry_dsn": settings.SENTRY_DSN,
        "sentry_environment": settings.SENTRY_ENVIRONMENT,
        "sentry_release": settings.SENTRY_RELEASE,
    }


def google(request):
    return {
        "google_api_key": settings.GOOGLE_API_KEY,
    }
