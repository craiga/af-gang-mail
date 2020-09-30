"""Test create_email_message."""

from django import urls

import pytest

from af_gang_mail.views import MailSent


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
    assert (
        urls.reverse("draw-sent", kwargs={"slug": exchange.slug}) in email_message.body
    )
