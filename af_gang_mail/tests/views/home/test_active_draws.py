"""Home page tests."""

# pylint: disable=redefined-outer-name

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
def recipient():
    return baker.make("af_gang_mail.User")


@pytest.fixture
def draw(exchange, user, recipient):
    return baker.make(
        "af_gang_mail.Draw", exchange=exchange, sender=user, recipient=recipient
    )


@pytest.mark.django_db
def test_active_draws(view, rf, user, exchange, draw, recipient):
    """Test list of active exchanges."""

    request = rf.get("/")
    request.user = user
    response = view(request)
    assert response.context_data["active_draws"] == [(exchange, recipient)]


@pytest.mark.django_db
def test_not_drawn(view, rf, user, exchange, recipient):
    """Test list of active exchanges when user was not drawn."""

    request = rf.get("/")
    request.user = user
    response = view(request)
    assert response.context_data["active_draws"] == []
