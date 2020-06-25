"""Test Select Exchanges form."""

import pytest

from af_gang_mail.forms import SelectExchanges


@pytest.mark.django_db
def test_only_future_exchanges(user, future_exchanges):
    """Test that only future exchanges are available for selection."""

    form = SelectExchanges(instance=user)
    assert [e.id for e in form.fields["exchanges"].queryset] == [
        e.id for e in future_exchanges.order_by("drawn")
    ]
