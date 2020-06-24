"""Fixtures for home view tests."""

import pytest

from af_gang_mail.views import Home


@pytest.fixture
def view():
    return Home.as_view()
