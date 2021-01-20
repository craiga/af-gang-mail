"""Test scheduled_for_confirmation."""

# pylint: disable=redefined-outer-name, unused-argument

from datetime import timedelta

from django.utils.timezone import now

import pytest
from model_bakery import baker

from af_gang_mail.models import Exchange


@pytest.fixture
def due_for_confirmation_exchanges():
    """Exchanges due to be confirmed."""

    due_for_confirmation_exchanges = []
    for i in range(0, 3):
        due_for_confirmation_exchanges.append(
            baker.make(
                "af_gang_mail.Exchange",
                name=f"Due for Confirmation Exchange { i + 1 }",
                slug=f"due-exchange-{ i + 1 }",
                confirmation_started=None,
                confirmation=now() - timedelta(seconds=i),
            )
        )

    return due_for_confirmation_exchanges


@pytest.fixture
def confirmed_exchanges():
    """Confirmed exchanges."""

    confirmed_exchanges = []
    for i in range(0, 3):
        confirmed_exchanges.append(
            baker.make(
                "af_gang_mail.Exchange",
                name=f"Confirmed Exchange { i + 1 }",
                slug=f"confirmed-exchange-{ i + 1 }",
                confirmation_started=now() - timedelta(hours=i),
                confirmation=now() - timedelta(minutes=i),
            )
        )

    return confirmed_exchanges


@pytest.fixture
def not_due_for_confirmation_exchanges():
    """Exchanges which aren't yet due to be confirmed."""

    not_due_for_confirmation_exchanges = []
    for i in range(0, 3):
        not_due_for_confirmation_exchanges.append(
            baker.make(
                "af_gang_mail.Exchange",
                name=f"Not Due for Confirmation Exchange { i + 1 }",
                slug=f"not-due-exchange-{ i + 1 }",
                confirmation_started=None,
                confirmation=now() + timedelta(minutes=i + 1),
            )
        )

    return not_due_for_confirmation_exchanges


@pytest.fixture
def no_confirmation_exchanges():
    """Exchanges with no confirmation date."""

    no_confirmation_exchanges = []
    for i in range(0, 3):
        no_confirmation_exchanges.append(
            baker.make(
                "af_gang_mail.Exchange",
                name=f"Confirmed Exchange { i + 1 }",
                slug=f"confirmed-exchange-{ i + 1 }",
                confirmation_started=None,
                confirmation=None,
            )
        )

    return no_confirmation_exchanges


@pytest.mark.django_db
def test_scheduled_for_confirmation(
    due_for_confirmation_exchanges,
    confirmed_exchanges,
    not_due_for_confirmation_exchanges,
    no_confirmation_exchanges,
):
    """Test scheduled_for_confirmation."""

    exchanges = Exchange.objects.scheduled_for_confirmation()
    assert exchanges.count() == len(due_for_confirmation_exchanges)
    for exchange in exchanges:
        assert exchange in due_for_confirmation_exchanges
