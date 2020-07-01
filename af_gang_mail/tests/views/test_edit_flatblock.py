"""Test edit flat block view."""

# pylint: disable=redefined-outer-name

from http import HTTPStatus

from django import urls
from django.contrib.auth.models import Permission

import pytest
from model_bakery import baker


@pytest.fixture
def flatblock():
    return baker.make("flatblocks.Flatblock")


@pytest.mark.django_db
def test_edit(flatblock, user, client):
    """Test that a user with permission can edit a flat block."""

    user.user_permissions.add(Permission.objects.get(codename="change_flatblock"))
    client.force_login(user)
    response = client.get(urls.reverse("edit-flatblock", kwargs={"pk": flatblock.id}))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_edit_no_permission(flatblock, user, client):
    """Test that a user without permission cannot edit a flat block."""

    client.force_login(user)
    response = client.get(urls.reverse("edit-flatblock", kwargs={"pk": flatblock.id}))
    assert response.status_code == HTTPStatus.FOUND
