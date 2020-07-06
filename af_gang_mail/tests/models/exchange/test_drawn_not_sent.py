"""Test drawn_not_sent."""

# pylint: disable=redefined-outer-name, unused-argument

from datetime import timedelta

from django.utils.timezone import now

import pytest
from model_bakery import baker

from af_gang_mail.models import Exchange


@pytest.fixture
def exchanges_drawn_not_sent():
    """Exchanges which are drawn but not sent."""

    exchanges = []
    for i in range(0, 3):
        exchanges.append(
            baker.make(
                "af_gang_mail.Exchange",
                name=f"Drawn Not Sent Exchange { i + 1 }",
                slug=f"drawn-not-sent-exchange-{ i + 1 }",
                drawn=now() - timedelta(days=i + 1),
                sent=now() + timedelta(days=i + 1),
            )
        )

    return exchanges


@pytest.fixture
def exchanges_not_drawn():
    """Exchanges which haven't been drawn."""

    exchanges = []
    for i in range(0, 3):
        exchanges.append(
            baker.make(
                "af_gang_mail.Exchange",
                name=f"Not Drawn Exchange { i + 1 }",
                slug=f"not-drawn-exchange-{ i + 1 }",
                drawn=now() + timedelta(days=i + 1),
                sent=now() + timedelta(days=i + 2),
            )
        )

    return exchanges


@pytest.fixture
def exchanges_sent():
    """Exchanges which have already been sent."""

    exchanges = []
    for i in range(0, 3):
        exchanges.append(
            baker.make(
                "af_gang_mail.Exchange",
                name=f"Sent Exchange { i + 1 }",
                slug=f"sent-exchange-{ i + 1 }",
                drawn=now() - timedelta(days=i + 2),
                sent=now() - timedelta(days=i + 1),
            )
        )

    return exchanges


@pytest.mark.django_db
def test_drawn_not_sent(exchanges_drawn_not_sent, exchanges_not_drawn, exchanges_sent):
    """Test drawn_not_sent."""

    exchanges = Exchange.objects.drawn_not_sent()
    assert exchanges.count() == len(exchanges_drawn_not_sent)
    for exchange in exchanges:
        assert exchange in exchanges_drawn_not_sent
