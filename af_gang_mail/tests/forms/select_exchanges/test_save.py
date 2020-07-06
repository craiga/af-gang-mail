"""Test Select Exchanges form saving."""

import pytest

from af_gang_mail.forms import SelectExchanges


@pytest.mark.django_db
def test_preserves_old_selections(
    user, past_exchanges, current_exchanges, upcoming_exchanges
):
    """Test previously selected exchanges which aren't upcoming are preserved."""

    assert (
        user.exchanges.count()
        == past_exchanges.count()
        + current_exchanges.count()
        + upcoming_exchanges.count()
    )
    assert upcoming_exchanges.count() > 1

    form = SelectExchanges(
        instance=user, data={"exchanges": [upcoming_exchanges[0].id]}
    )
    assert form.is_valid()
    form.save()

    user.refresh_from_db()
    assert (
        user.exchanges.count() == past_exchanges.count() + current_exchanges.count() + 1
    )
