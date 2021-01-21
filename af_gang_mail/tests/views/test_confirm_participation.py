"""Tests for confirming participation in draw."""

# pylint: disable=redefined-outer-name

from django.core.exceptions import PermissionDenied

import pytest

from af_gang_mail import models, views


@pytest.fixture
def view():
    return views.ConfirmParticipation.as_view()


@pytest.fixture
def upcoming_exchange(upcoming_exchanges):
    return upcoming_exchanges[0]


@pytest.fixture
def other_upcoming_exchange(other_upcoming_exchanges):
    return other_upcoming_exchanges[0]


@pytest.fixture
def user_in_upcoming_exchange(user, upcoming_exchange):
    return models.UserInExchange.objects.get(exchange=upcoming_exchange, user=user)


@pytest.mark.django_db
def test_confirm(view, rf, user, upcoming_exchange, user_in_upcoming_exchange):
    """Test confirming participation in draw."""

    assert not user_in_upcoming_exchange.confirmed

    request = rf.get("/")
    request.user = user
    view(request, slug=upcoming_exchange.slug)

    user_in_upcoming_exchange.refresh_from_db()
    assert user_in_upcoming_exchange.confirmed


@pytest.mark.django_db
def test_not_in_exchange(view, rf, user, other_upcoming_exchange):
    """User not in exchange."""

    request = rf.get("/")
    request.user = user
    with pytest.raises(PermissionDenied):
        view(request, slug=other_upcoming_exchange.slug)
