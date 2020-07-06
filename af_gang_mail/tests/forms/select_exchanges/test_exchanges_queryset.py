"""Test Select Exchanges queryset."""

import pytest

from af_gang_mail.forms import SelectExchanges


@pytest.mark.django_db
def test_exchanges(user, upcoming_exchanges):
    """Test that only upcoming exchanges are available for selection."""

    form = SelectExchanges(instance=user)
    assert [e.id for e in form.fields["exchanges"].queryset] == [
        e.id for e in upcoming_exchanges.order_by("drawn")
    ]
