"""Test create_email_message."""

# pylint: disable=redefined-outer-name

import pytest
from model_bakery import baker

from af_gang_mail.views import MailSent


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


@pytest.mark.django_db
def test_create_email_message(draw, exchange, recipient, sender):
    """Test create_email_message."""

    view = MailSent()

    email_message = view.create_email_message(draw, "test message")

    assert [recipient.email] == email_message.to

    assert sender.get_full_name() in email_message.subject
    assert exchange.name in email_message.subject

    assert recipient.get_full_name() in email_message.body
    assert sender.get_full_name() in email_message.body
    assert exchange.name in email_message.body
    assert "test message" in email_message.body
