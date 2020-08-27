"""Test eligible_for_draw."""

# pylint: disable=redefined-outer-name

import pytest
from allauth.account.models import EmailAddress
from model_bakery import baker

from af_gang_mail.models import User


@pytest.fixture
def user():
    """A user."""

    return baker.make(
        "af_gang_mail.User",
        emailaddress_set=baker.prepare(EmailAddress, verified=True, _quantity=1),
        _fill_optional=["first_name", "last_name"],
    )


@pytest.fixture
def unverified_user():
    """An unverified user."""

    return baker.make(
        "af_gang_mail.User",
        emailaddress_set=baker.prepare(EmailAddress, verified=False, _quantity=1),
        _fill_optional=["first_name", "last_name"],
    )


@pytest.fixture
def no_name_user():
    """A user with no name."""

    return baker.make(
        "af_gang_mail.User",
        first_name="",
        last_name="",
        emailaddress_set=baker.prepare(EmailAddress, verified=True, _quantity=1),
    )


@pytest.fixture
def first_name_user():
    """A user with no last name."""
    return baker.make(
        "af_gang_mail.User",
        last_name="",
        emailaddress_set=baker.prepare(EmailAddress, verified=True, _quantity=1),
        _fill_optional=["first_name"],
    )


@pytest.fixture
def last_name_user():
    """A user with no first name."""
    return baker.make(
        "af_gang_mail.User",
        first_name="",
        emailaddress_set=baker.prepare(EmailAddress, verified=True, _quantity=1),
        _fill_optional=["last_name"],
    )


@pytest.mark.django_db
# pylint: disable=unused-argument
def test_eligible_for_draw(
    user, first_name_user, last_name_user, unverified_user, no_name_user
):
    """Test getting users which are eligible for a draw."""

    expected_users = set([user, first_name_user, last_name_user])
    assert expected_users == set(User.objects.eligible_for_draw())
