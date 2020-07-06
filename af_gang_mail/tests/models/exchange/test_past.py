"""Test past."""

# pylint: disable=redefined-outer-name, unused-argument

from datetime import timedelta

from django.utils.timezone import now

import pytest
from model_bakery import baker

from af_gang_mail.models import Exchange


@pytest.fixture
def past_exchanges():
    """Past exchanges."""

    exchanges = []
    for i in range(0, 3):
        exchanges.append(
            baker.make(
                "af_gang_mail.Exchange",
                name=f"Past Exchange { i + 1 }",
                slug=f"past-exchange-{ i + 1 }",
                received=now() - timedelta(days=i + 1),
            )
        )

    return exchanges


@pytest.fixture
def not_past_exchanges():
    """Exchanges aren't past."""

    exchanges = []
    for i in range(0, 3):
        exchanges.append(
            baker.make(
                "af_gang_mail.Exchange",
                name=f"Not Past Exchange { i + 1 }",
                slug=f"not-past-exchange-{ i + 1 }",
                received=now() + timedelta(days=i + 1),
            )
        )

    return exchanges


@pytest.mark.django_db
def test_past(past_exchanges, not_past_exchanges):
    """Test past."""

    exchanges = Exchange.objects.past()
    assert exchanges.count() == len(past_exchanges)
    for exchange in exchanges:
        assert exchange in past_exchanges
