"""User exchange get method tests."""

import pytest


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
