"""Tests for draw view."""

from django.core.exceptions import PermissionDenied

import pytest
from model_bakery import baker

from af_gang_mail.views import Draw


@pytest.fixture
def view():
    return Draw.as_view()


@pytest.fixture
def recipient(drawn_not_sent_exchange, user):
    recipient = baker.make("af_gang_mail.User")
    baker.make("af_gang_mail.Draw", exchange=drawn_not_sent_exchange, sender=user, recipient=recipient)
    return recipient


@pytest.mark.django_db
def test(view, rf, user, drawn_not_sent_exchange, recipient):
    """Test draw view."""

    request = rf.get("/")
    request.user = user
    view(request, slug=drawn_not_sent_exchange.slug)


@pytest.mark.django_db
def test_not_drawn(view, rf, user, drawn_not_sent_exchange):
    """User is in the exchange but didn't validate their email address so wasn't drawn."""

    request = rf.get("/")
    request.user = user
    with pytest.raises(PermissionDenied):
        view(request, slug=drawn_not_sent_exchange.slug)


@pytest.mark.django_db
def test_not_in_exchange(view, rf, drawn_not_sent_exchange):
    """User not in exchange."""

    request = rf.get("/")
    request.user = baker.make("af_gang_mail.User")
    with pytest.raises(PermissionDenied):
        view(request, slug=drawn_not_sent_exchange.slug)
