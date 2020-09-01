"""Test Select Exchanges queryset."""

# pylint: disable=unused-argument

import pytest

from af_gang_mail.forms import SelectExchanges


@pytest.mark.django_db
def test_exchanges(user, upcoming_exchanges, past_exchanges):
    """Test that only upcoming exchanges are available for selection."""

    form = SelectExchanges(instance=user)
    assert [e.id for e in form.fields["exchanges"].queryset] == [
        e.id for e in upcoming_exchanges.order_by("drawn")
    ]


@pytest.mark.django_db
def test_exchanges_jump_in_time(user, upcoming_exchanges, past_exchanges, freezer):
    """Upcoming filtering works even when the form was instantiated a while ago."""

    freezer.move_to("2099-01-01")
    form = SelectExchanges(instance=user)
    assert form.fields["exchanges"].queryset.count() == 0
