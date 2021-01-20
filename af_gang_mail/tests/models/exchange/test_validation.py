"""Test exchange model validation."""

from datetime import timedelta

from django.core.exceptions import ValidationError
from django.utils.timezone import now

import pytest
from model_bakery import baker


@pytest.mark.parametrize(
    "confirmation, confirmation_reminder, drawn, sent, received",
    [
        (
            now(),
            now() + timedelta(days=1),
            now() + timedelta(days=2),
            now() + timedelta(days=3),
            now() + timedelta(days=4),
        ),
    ],
)
@pytest.mark.django_db
def test_valid_datetime_sequence(
    confirmation, confirmation_reminder, drawn, sent, received
):
    """Test a valid datetime sequence."""

    exchange = baker.prepare(
        "af_gang_mail.Exchange",
        slug="my-cool-exchange",
        confirmation=confirmation,
        confirmation_reminder=confirmation_reminder,
        drawn=drawn,
        sent=sent,
        received=received,
    )
    exchange.full_clean()


@pytest.mark.parametrize(
    "confirmation, confirmation_reminder, drawn, sent, received",
    [
        (
            now() + timedelta(days=1),
            now(),
            now() + timedelta(days=2),
            now() + timedelta(days=3),
            now() + timedelta(days=4),
        ),
        (
            now() + timedelta(days=1),
            now() + timedelta(days=2),
            now(),
            now() + timedelta(days=3),
            now() + timedelta(days=4),
        ),
        (
            now() + timedelta(days=1),
            now() + timedelta(days=2),
            now() + timedelta(days=3),
            now(),
            now() + timedelta(days=4),
        ),
        (
            now() + timedelta(days=1),
            now() + timedelta(days=2),
            now() + timedelta(days=3),
            now() + timedelta(days=4),
            now(),
        ),
    ],
)
@pytest.mark.django_db
def test_invalid_datetime_sequence(
    confirmation, confirmation_reminder, drawn, sent, received
):
    """Test an invalid datetime sequence."""

    exchange = baker.prepare(
        "af_gang_mail.Exchange",
        slug="my-cool-exchange",
        confirmation=confirmation,
        confirmation_reminder=confirmation_reminder,
        drawn=drawn,
        sent=sent,
        received=received,
    )
    with pytest.raises(ValidationError):
        exchange.full_clean()
