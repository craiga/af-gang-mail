"""Test scheduled_for_confirmation_reminder."""

# pylint: disable=redefined-outer-name, unused-argument

from datetime import timedelta

from django.utils.timezone import now

import pytest
from model_bakery import baker

from af_gang_mail.models import Exchange


@pytest.fixture
def due_for_confirmation_reminder_exchanges():
    """Exchanges due to for confirmation reminder."""

    due_for_confirmation_reminder_exchanges = []
    for i in range(0, 3):
        due_for_confirmation_reminder_exchanges.append(
            baker.make(
                "af_gang_mail.Exchange",
                name=f"Due for Confirmation Reminder Exchange { i + 1 }",
                slug=f"due-exchange-{ i + 1 }",
                confirmation_reminder_started=None,
                confirmation_reminder=now() - timedelta(seconds=i),
            )
        )

    return due_for_confirmation_reminder_exchanges


@pytest.fixture
def confirmation_reminder_exchanges():
    """confirmation_reminder exchanges."""

    confirmation_reminder_exchanges = []
    for i in range(0, 3):
        confirmation_reminder_exchanges.append(
            baker.make(
                "af_gang_mail.Exchange",
                name=f"confirmation_reminder Exchange { i + 1 }",
                slug=f"confirmation_reminder-exchange-{ i + 1 }",
                confirmation_reminder_started=now() - timedelta(hours=i),
                confirmation_reminder=now() - timedelta(minutes=i),
            )
        )

    return confirmation_reminder_exchanges


@pytest.fixture
def not_due_exchanges():
    """Exchanges which aren't yet due to be confirmation_reminder."""

    not_due_exchanges = []
    for i in range(0, 3):
        not_due_exchanges.append(
            baker.make(
                "af_gang_mail.Exchange",
                name=f"Not Due for Confirmation Exchange { i + 1 }",
                slug=f"not-due-exchange-{ i + 1 }",
                confirmation_reminder_started=None,
                confirmation_reminder=now() + timedelta(minutes=i + 1),
            )
        )

    return not_due_exchanges


@pytest.fixture
def no_confirmation_reminder_exchanges():
    """Exchanges with no confirmation reminder date."""

    no_confirmation_reminder_exchanges = []
    for i in range(0, 3):
        no_confirmation_reminder_exchanges.append(
            baker.make(
                "af_gang_mail.Exchange",
                name=f"Confirmed Exchange { i + 1 }",
                slug=f"confirmed-exchange-{ i + 1 }",
                confirmation_reminder_started=None,
                confirmation_reminder=None,
            )
        )

    return no_confirmation_reminder_exchanges


@pytest.mark.django_db
def test_scheduled_for_confirmation_reminder(
    due_for_confirmation_reminder_exchanges,
    confirmation_reminder_exchanges,
    not_due_exchanges,
):
    """Test scheduled_for_confirmation_reminder."""

    exchanges = Exchange.objects.scheduled_for_confirmation_reminder()
    assert exchanges.count() == len(due_for_confirmation_reminder_exchanges)
    for exchange in exchanges:
        assert exchange in due_for_confirmation_reminder_exchanges
