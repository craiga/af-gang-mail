"""Test upcoming."""

# pylint: disable=redefined-outer-name, unused-argument

from datetime import timedelta

from django.utils.timezone import now

import pytest
from model_bakery import baker

from af_gang_mail.models import Exchange


@pytest.fixture
def upcoming_exchanges():
    """Upcoming exchanges."""

    exchanges = []
    for i in range(0, 3):
        exchanges.append(
            baker.make(
                "af_gang_mail.Exchange",
                name=f"Upcoming Exchange { i + 1 }",
                slug=f"upcoming-exchange-{ i + 1 }",
                drawn=now() + timedelta(days=i + 1),
            )
        )

    return exchanges


@pytest.fixture
def not_upcoming_exchanges():
    """Exchanges aren't upcoming."""

    exchanges = []
    for i in range(0, 3):
        exchanges.append(
            baker.make(
                "af_gang_mail.Exchange",
                name=f"Not Upcoming Exchange { i + 1 }",
                slug=f"not-upcoming-exchange-{ i + 1 }",
                drawn=now() - timedelta(days=i),
            )
        )

    return exchanges


@pytest.mark.django_db
def test_upcoming(upcoming_exchanges, not_upcoming_exchanges):
    """Test upcoming."""

    exchanges = Exchange.objects.upcoming()
    assert exchanges.count() == len(upcoming_exchanges)
    for exchange in exchanges:
        assert exchange in upcoming_exchanges


@pytest.mark.django_db
def test_not_upcoming(upcoming_exchanges, not_upcoming_exchanges):
    """Test not_upcoming."""

    exchanges = Exchange.objects.not_upcoming()
    assert exchanges.count() == len(not_upcoming_exchanges)
    for exchange in exchanges:
        assert exchange in not_upcoming_exchanges


@pytest.mark.freeze_time
@pytest.mark.django_db
def test_due_in_one_minute():
    """Test an exchange to be drawn in a minute isn't upcoming."""

    baker.make(
        "af_gang_mail.Exchange",
        slug="my-cool-exchange",
        drawn=now() + timedelta(minutes=1),
    )
    assert Exchange.objects.upcoming().count() == 0
