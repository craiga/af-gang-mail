"""Test scheduled_for_draw."""

# pylint: disable=redefined-outer-name, unused-argument

from datetime import timedelta

from django.utils.timezone import now

import pytest
from model_bakery import baker

from af_gang_mail.models import Exchange


@pytest.fixture
def due_exchanges():
    """Exchanges due to be drawn."""

    exchanges = []
    for i in range(0, 3):
        exchanges.append(
            baker.make(
                "af_gang_mail.Exchange",
                name=f"Due Exchange { i + 1 }",
                slug=f"due-exchange-{ i + 1 }",
                draw_started=None,
                drawn=now() - timedelta(seconds=i),
            )
        )

    return exchanges


@pytest.fixture
def drawn_exchanges():
    """Drawn exchanges."""

    exchanges = []
    for i in range(0, 3):
        exchanges.append(
            baker.make(
                "af_gang_mail.Exchange",
                name=f"Drawn Exchange { i + 1 }",
                slug=f"drawn-exchange-{ i + 1 }",
                draw_started=now() - timedelta(hours=i),
                drawn=now() - timedelta(minutes=i),
            )
        )

    return exchanges


@pytest.fixture
def not_due_exchanges():
    """Exchanges which aren't yet due to be drawn."""

    exchanges = []
    for i in range(0, 3):
        exchanges.append(
            baker.make(
                "af_gang_mail.Exchange",
                name=f"Not Due Exchange { i + 1 }",
                slug=f"not-due-exchange-{ i + 1 }",
                draw_started=None,
                drawn=now() + timedelta(minutes=i + 1),
            )
        )

    return exchanges


@pytest.mark.django_db
def test_scheduled_for_draw(due_exchanges, drawn_exchanges, not_due_exchanges):
    """Test scheduled_for_draw."""

    exchanges = Exchange.objects.scheduled_for_draw()
    assert exchanges.count() == len(due_exchanges)
    for exchange in exchanges:
        assert exchange in due_exchanges
