"""Test as_email_message."""

# pylint: disable=redefined-outer-name

from django import urls

import pytest
from model_bakery import baker


@pytest.fixture
def draw():
    return baker.prepare("af_gang_mail.Draw", exchange__slug="my-cool-exchange")


@pytest.mark.django_db
def test_as_email_message(draw):
    """Test as_email_message."""

    email_message = draw.as_email_message()

    assert [draw.sender.email] == email_message.to

    assert draw.exchange.name in email_message.subject

    assert draw.exchange.name in email_message.body
    assert draw.recipient.get_full_name() in email_message.body
    assert draw.recipient.get_full_address() in email_message.body
    assert (
        urls.reverse("draw", kwargs={"slug": draw.exchange.slug}) in email_message.body
    )
    assert "http" in email_message.body
