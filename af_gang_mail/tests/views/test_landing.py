"""Landing page redirection tests."""

# pylint: disable=redefined-outer-name

from http import HTTPStatus

from django.contrib.auth.models import AnonymousUser, Permission

import pytest
from model_bakery import baker

from af_gang_mail.views import Landing


@pytest.fixture
def view():
    return Landing.as_view()


@pytest.fixture
def anonymous_user():
    return AnonymousUser()


@pytest.fixture
def user_name_kwargs():
    return {"first_name": "Joe", "last_name": "Talbot"}


@pytest.fixture
def user_address_kwargs():
    return {
        "address_line_1": "1049 Gotho Road",
        "address_city": "Bristol",
        "address_country": "GB",
    }


@pytest.fixture
def user_no_exchanges(user_name_kwargs, user_address_kwargs):
    return baker.make("af_gang_mail.User", **user_name_kwargs, **user_address_kwargs)


@pytest.fixture
def user_with_name(user_name_kwargs):
    return baker.prepare("af_gang_mail.User", **user_name_kwargs)


@pytest.fixture
def user_with_address(user_address_kwargs):
    return baker.prepare("af_gang_mail.User", **user_address_kwargs)


def test_unauthentated(view, anonymous_user, rf):
    """Not redirected when unauthenticated."""

    request = rf.get("/")
    request.user = anonymous_user
    response = view(request)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_authenticated(view, user, rf):
    """Redirected when logged in."""

    request = rf.get("/")
    request.user = user
    response = view(request)
    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db
def test_flatblock_editor(view, user, rf):
    """Test user not redirected when logged in as a flat blocks editor."""

    user.user_permissions.add(Permission.objects.get(codename="change_flatblock"))
    request = rf.get("/")
    request.user = user
    response = view(request)
    assert response.status_code == HTTPStatus.OK
