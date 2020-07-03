"""User exchange get method tests."""

import pytest
from allauth.account.models import EmailAddress
from model_bakery import baker


@pytest.mark.django_db
def test_get_past_exchanges(user, past_exchanges):
    """Test that past exchanges are retrieved as expected."""

    assert [e.id for e in user.get_past_exchanges()] == [e.id for e in past_exchanges]


@pytest.mark.django_db
def test_get_current_exchanges(user, current_exchanges):
    """Test that current exchanges are retrieved as expected."""

    assert [e.id for e in user.get_current_exchanges()] == [
        e.id for e in current_exchanges
    ]


@pytest.mark.django_db
def test_get_future_exchanges(user, future_exchanges):
    """Test that future exchanges are retrieved as expected."""

    assert [e.id for e in user.get_future_exchanges()] == [
        e.id for e in future_exchanges
    ]


@pytest.mark.django_db
def test_has_verified_email_address(user):
    """Test has_verified_email_address."""

    baker.make(EmailAddress, user=user, verified=False)
    baker.make(EmailAddress, user=user, verified=True)
    baker.make(EmailAddress, user=user, verified=False)
    assert user.has_verified_email_address()


@pytest.mark.django_db
def test_does_not_have_verified_email_address(user):
    """Test has_verified_email_address when user doesn't have a verified email address."""

    baker.make(EmailAddress, user=user, verified=False)
    baker.make(EmailAddress, user=user, verified=False)
    baker.make(EmailAddress, user=user, verified=False)
    assert not user.has_verified_email_address()


@pytest.mark.django_db
def test_no_email_address(user):
    """Test has_verified_email_address when user doesn't have an email address."""

    assert not user.has_verified_email_address()
