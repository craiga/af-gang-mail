"""Exchange model tests."""

from datetime import timedelta

from django.core.exceptions import ValidationError
from django.utils.timezone import now

import pytest
from model_bakery import baker


@pytest.mark.django_db
def test_valid_datetime_sequence():
    """Test a valid datetime sequence."""

    exchange = baker.prepare(
        "af_gang_mail.Exchange",
        slug="my-cool-exchange",
        drawn=now(),
        sent=now() + timedelta(days=1),
        received=now() + timedelta(days=2),
    )
    exchange.full_clean()


@pytest.mark.parametrize(
    "drawn, sent, received",
    [
        (now() + timedelta(days=1), now(), now() + timedelta(days=2)),
        (now() + timedelta(days=1), now() + timedelta(days=2), now()),
    ],
)
@pytest.mark.django_db
def test_invalid_datetime_sequence(drawn, sent, received):
    """Test an invalid datetime sequence."""

    exchange = baker.prepare(
        "af_gang_mail.Exchange",
        slug="my-cool-exchange",
        drawn=drawn,
        sent=sent,
        received=received,
    )
    with pytest.raises(ValidationError):
        exchange.full_clean()
