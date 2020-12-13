"""Test as_created_email_message."""

# pylint: disable=redefined-outer-name

from django import urls

import pytest
from model_bakery import baker


@pytest.fixture
def exchange():
    return baker.make("af_gang_mail.Exchange", name="Really Cool", slug="really-cool")


@pytest.fixture
def user():
    return baker.make("af_gang_mail.User")


@pytest.fixture
def sender():
    return baker.make(
        "af_gang_mail.User",
        first_name="sender",
        last_name="senderson",
        _fill_optional=True,
    )


@pytest.fixture
def recipient():
    return baker.make(
        "af_gang_mail.User",
        first_name="recipient",
        last_name="Recipientson",
        _fill_optional=True,
    )


@pytest.fixture
def draw_as_sender(exchange, user, recipient):
    return baker.make(
        "af_gang_mail.Draw", exchange=exchange, sender=user, recipient=recipient
    )


@pytest.fixture
def draw_as_recipient(exchange, user, sender):
    return baker.make(
        "af_gang_mail.Draw", exchange=exchange, recipient=user, sender=sender
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "email_method",
    [
        "as_created_email_message",
        "as_send_reminder_email_message",
        "as_receive_reminder_email_message",
    ],
)
# pylint: disable=too-many-arguments,unused-argument
def test_email_message(
    email_method, draw_as_sender, draw_as_recipient, exchange, user, recipient, sender
):
    """Test as_created_email_message."""

    email_message = getattr(draw_as_sender, email_method)()

    assert [user.email] == email_message.to

    assert recipient.get_full_name()
    assert sender.get_full_name()

    assert exchange.name in email_message.subject

    assert exchange.name in email_message.body
    assert recipient.get_full_name() in email_message.body
    assert sender.get_full_name() in email_message.body
    assert sender.get_full_address() not in email_message.body
    assert urls.reverse("draw", kwargs={"slug": exchange.slug}) in email_message.body
    assert (
        urls.reverse("draw-sent", kwargs={"slug": exchange.slug}) in email_message.body
    )
    assert (
        urls.reverse("draw-received", kwargs={"slug": exchange.slug})
        in email_message.body
    )
    assert "http" in email_message.body
