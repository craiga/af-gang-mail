"""Test scheduled_for_send_reminder."""

# pylint: disable=redefined-outer-name, unused-argument

from datetime import timedelta

from django.utils.timezone import now

import pytest
from model_bakery import baker

from af_gang_mail.models import Exchange


@pytest.fixture
def due_for_send_reminder_exchanges():
    """Exchanges due to be sent."""

    due_for_send_reminder_exchanges = []
    for i in range(0, 3):
        due_for_send_reminder_exchanges.append(
            baker.make(
                "af_gang_mail.Exchange",
                name=f"Due for Send Reminder Exchange { i + 1 }",
                slug=f"due-exchange-{ i + 1 }",
                send_reminder_started=None,
                sent=now() - timedelta(seconds=i),
            )
        )

    return due_for_send_reminder_exchanges


@pytest.fixture
def sent_exchanges():
    """Sent exchanges."""

    sent_exchanges = []
    for i in range(0, 3):
        sent_exchanges.append(
            baker.make(
                "af_gang_mail.Exchange",
                name=f"Sent Exchange { i + 1 }",
                slug=f"Sent-exchange-{ i + 1 }",
                send_reminder_started=now() - timedelta(hours=i),
                sent=now() - timedelta(minutes=i),
            )
        )

    return sent_exchanges


@pytest.fixture
def not_due_for_send_reminder_exchanges():
    """Exchanges which aren't yet due to be sent."""

    not_due_for_send_reminder_exchanges = []
    for i in range(0, 3):
        not_due_for_send_reminder_exchanges.append(
            baker.make(
                "af_gang_mail.Exchange",
                name=f"Not Due for Send Reminder Exchange { i + 1 }",
                slug=f"not-due-exchange-{ i + 1 }",
                send_reminder_started=None,
                sent=now() + timedelta(minutes=i + 1),
            )
        )

    return not_due_for_send_reminder_exchanges


@pytest.mark.django_db
def test_scheduled_for_send_reminder(
    due_for_send_reminder_exchanges, sent_exchanges, not_due_for_send_reminder_exchanges
):
    """Test scheduled_for_send_reminder."""

    exchanges = Exchange.objects.scheduled_for_send_reminder()
    assert exchanges.count() == len(due_for_send_reminder_exchanges)
    for exchange in exchanges:
        assert exchange in due_for_send_reminder_exchanges
