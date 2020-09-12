"""Fixtures for views."""

# pylint: disable=redefined-outer-name

import pytest
from model_bakery import baker


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


@pytest.fixture
def exchange():
    return baker.prepare(
        "af_gang_mail.Exchange", name="Really Cool", slug="really-cool"
    )


@pytest.fixture
def sender():
    return baker.prepare(
        "af_gang_mail.User",
        first_name="Sender",
        last_name="Senderson",
        _fill_optional=True,
    )


@pytest.fixture
def recipient():
    return baker.prepare(
        "af_gang_mail.User",
        first_name="Recipient",
        last_name="Recipientson",
        _fill_optional=True,
    )


@pytest.fixture
def draw(exchange, sender, recipient):
    return baker.prepare(
        "af_gang_mail.Draw", exchange=exchange, sender=sender, recipient=recipient
    )
