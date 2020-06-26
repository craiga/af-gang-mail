"""Global pytest fixtures."""

# pylint: disable=redefined-outer-name

from datetime import timedelta

from django.utils.timezone import now

import pytest
from model_bakery import baker

from af_gang_mail import models


@pytest.fixture
def past_exchanges():
    """Exchanges in the past."""

    exchanges = []
    for i in range(1, 2):
        exchanges.append(
            baker.make(
                models.Exchange,
                name=f"Past {i}",
                slug=f"past-{i}",
                drawn=now() - timedelta(days=i * 10 + 6),
                sent=now() - timedelta(days=i * 10 + 3),
                received=now() - timedelta(days=i * 10),
            )
        )

    return models.Exchange.objects.filter(id__in=[e.id for e in exchanges])


@pytest.fixture
def current_exchanges():
    """Exchanges which are currently running."""

    exchanges = [
        baker.make(
            models.Exchange,
            name="Current 1",
            slug="current-1",
            drawn=now() - timedelta(days=1),
            sent=now() + timedelta(days=1),
            received=now() + timedelta(days=2),
        ),
        baker.make(
            models.Exchange,
            name="Current 2",
            slug="current-2",
            drawn=now() - timedelta(days=2),
            sent=now() - timedelta(days=1),
            received=now() + timedelta(days=1),
        ),
    ]

    return models.Exchange.objects.filter(id__in=[e.id for e in exchanges])


@pytest.fixture
def future_exchanges():
    """Exchanges in the future."""

    exchanges = []
    for i in range(2, 0, -1):
        exchanges.append(
            baker.make(
                models.Exchange,
                name=f"Future {i}",
                slug=f"future-{i}",
                drawn=now() + timedelta(days=i * 10),
                sent=now() + timedelta(days=i * 10 + 3),
                received=now() + timedelta(days=i * 10 + 6),
            )
        )

    return models.Exchange.objects.filter(id__in=[e.id for e in exchanges])


@pytest.fixture
def user(past_exchanges, current_exchanges, future_exchanges):
    """A user signed up to all the above exchanges."""

    user = baker.make(
        "af_gang_mail.User",
        first_name="Joe",
        last_name="Talbot",
        address_line_1="1049 Gotho Road",
        address_city="Bristol",
        address_country="GB",
    )
    user.exchanges.add(*past_exchanges)
    user.exchanges.add(*current_exchanges)
    user.exchanges.add(*future_exchanges)
    return user
