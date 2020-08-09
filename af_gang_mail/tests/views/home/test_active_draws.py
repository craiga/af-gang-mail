"""Home page tests."""

# pylint: disable=redefined-outer-name, too-many-arguments

from datetime import timedelta

from django.utils.timezone import now

import pytest
from model_bakery import baker

from af_gang_mail.views import Home


@pytest.fixture
def view():
    return Home.as_view()


@pytest.fixture
def exchange():
    """An exchange which is drawn but not sent."""

    return baker.make(
        "af_gang_mail.Exchange",
        slug="my-cool-exchange",
        drawn=now() - timedelta(days=1),
        sent=now() + timedelta(days=1),
    )


@pytest.fixture
def user(exchange):
    user = baker.make("af_gang_mail.User")
    user.exchanges.add(exchange)
    return user


@pytest.fixture
def draw_as_sender(exchange, user):
    return baker.make("af_gang_mail.Draw", exchange=exchange, sender=user)


@pytest.fixture
def draw_as_recipient(exchange, user):
    return baker.make("af_gang_mail.Draw", exchange=exchange, recipient=user)


@pytest.mark.django_db
def test_active_draws(view, rf, user, exchange, draw_as_sender, draw_as_recipient):
    """Test list of active exchanges."""

    request = rf.get("/")
    request.user = user
    response = view(request)
    assert response.context_data["active_draws"] == [
        (exchange, draw_as_sender.recipient, draw_as_recipient.sender)
    ]


@pytest.mark.django_db
def test_not_drawn(view, rf, user, exchange):  # pylint: disable=unused-argument
    """Test list of active exchanges when user was not drawn."""

    request = rf.get("/")
    request.user = user
    response = view(request)
    assert response.context_data["active_draws"] == []
