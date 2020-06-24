"""View tests."""

# pylint: disable=redefined-outer-name

from http import HTTPStatus

from django import urls
from django.contrib.auth.models import AnonymousUser

import pytest
from model_bakery import baker


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
def user_complete(user_name_kwargs, user_address_kwargs):
    return baker.prepare("af_gang_mail.User", **user_name_kwargs, **user_address_kwargs)


@pytest.fixture
def user_with_name(user_name_kwargs):
    return baker.prepare("af_gang_mail.User", **user_name_kwargs)


@pytest.fixture
def user_with_address(user_address_kwargs):
    return baker.prepare("af_gang_mail.User", **user_address_kwargs)


def test_empty_name(view, user_with_address, rf):
    """Redirected to update name and address when name is empty."""

    request = rf.get("/")
    request.user = user_with_address
    response = view(request)

    assert response.status_code == HTTPStatus.FOUND
    assert response["Location"] == urls.reverse("update-name-and-address")


def test_empty_address(view, user_with_name, rf):
    """Redirected to update name and address when address is empty."""

    request = rf.get("/")
    request.user = user_with_name
    response = view(request)

    assert response.status_code == HTTPStatus.FOUND
    assert response["Location"] == urls.reverse("update-name-and-address")


def test_unauthentated(view, anonymous_user, rf):
    """Not redirected when unauthenticated."""

    request = rf.get("/")
    request.user = anonymous_user
    response = view(request)
    assert response.status_code == HTTPStatus.OK


def test_all_details(view, user_complete, rf):
    """Not redirected when logged in with all details."""

    request = rf.get("/")
    request.user = user_complete
    response = view(request)
    assert response.status_code == HTTPStatus.OK
