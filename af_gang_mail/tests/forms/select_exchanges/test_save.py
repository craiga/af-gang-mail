"""Test Select Exchanges form saving."""

from datetime import timedelta

from django.utils.timezone import now

import pytest
from model_bakery import baker

from af_gang_mail import forms, models


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

    form = forms.SelectExchanges(
        instance=user, data={"exchanges": [upcoming_exchanges[0].id]}
    )
    assert form.is_valid()
    form.save()

    user.refresh_from_db()
    assert (
        user.exchanges.count() == past_exchanges.count() + current_exchanges.count() + 1
    )


@pytest.mark.django_db
def test_confirmation(user):
    """Test that joining an exchange after its confirmation reminder."""

    tomorrow = baker.make(
        "af_gang_mail.Exchange",
        slug="tomorrow",
        confirmation_reminder=now() - timedelta(days=1),
        drawn=now() + timedelta(days=1),
    )
    day_after_tomorrow = baker.make(
        "af_gang_mail.Exchange",
        slug="day-after-tomorrow",
        confirmation_reminder=now() + timedelta(days=1),
        drawn=now() + timedelta(days=2),
    )

    form = forms.SelectExchanges(
        instance=user, data={"exchanges": [tomorrow.id, day_after_tomorrow.id]}
    )

    assert form.is_valid()
    form.save()

    user.refresh_from_db()

    user_in_tomorrow = models.UserInExchange.objects.get(user=user, exchange=tomorrow)
    assert user_in_tomorrow.confirmed

    user_in_day_after_tomorrow = models.UserInExchange.objects.get(
        user=user, exchange=day_after_tomorrow
    )
    assert not user_in_day_after_tomorrow.confirmed
