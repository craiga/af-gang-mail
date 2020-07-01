"""Fixtures for views."""

import pytest


@pytest.fixture(autouse=True)
def static_file_storage(settings):
    """
    Reconfigure static files storage.

    This is to avoid errors relating to missing static files manifest entries.
    """

    settings.STATICFILES_STORAGE = (
        "django.contrib.staticfiles.storage.StaticFilesStorage"
    )


@pytest.fixture(autouse=True)
def disable_https_redirect(settings):
    """Disable the HTTPS redirect."""

    settings.SECURE_SSL_REDIRECT = False
