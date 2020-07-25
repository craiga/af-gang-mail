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
def drawn_not_sent_exchange():
    return baker.make(
        models.Exchange,
        name="Drawn Not Sent",
        slug="drawn-not-sent",
        drawn=now() - timedelta(days=1),
        sent=now() + timedelta(days=1),
        received=now() + timedelta(days=2),
    )


@pytest.fixture
def sent_not_received_exchange():
    return baker.make(
        models.Exchange,
        name="Sent Not Received",
        slug="sent-not-received",
        drawn=now() - timedelta(days=2),
        sent=now() - timedelta(days=1),
        received=now() + timedelta(days=1),
    )


@pytest.fixture
def current_exchanges(drawn_not_sent_exchange, sent_not_received_exchange):
    """Exchanges which are currently running."""

    ids = [drawn_not_sent_exchange.id, sent_not_received_exchange.id]
    return models.Exchange.objects.filter(id__in=ids)


@pytest.fixture
def upcoming_exchanges():
    """Upcoming exchanges."""

    exchanges = []
    for i in range(2, 0, -1):
        exchanges.append(
            baker.make(
                models.Exchange,
                name=f"Upcoming {i}",
                slug=f"upcoming-{i}",
                drawn=now() + timedelta(days=i * 10),
                sent=now() + timedelta(days=i * 10 + 3),
                received=now() + timedelta(days=i * 10 + 6),
            )
        )

    return models.Exchange.objects.filter(id__in=[e.id for e in exchanges])


@pytest.fixture
def user(past_exchanges, current_exchanges, upcoming_exchanges):
    """A user signed up to all the above exchanges."""

    user = baker.make(
        "af_gang_mail.User",
        first_name="Joe",
        last_name="Talbot",
        street_address="1049 Gotho Road",
        address_city="Bristol",
        address_country="GB",
    )
    user.exchanges.add(*past_exchanges)
    user.exchanges.add(*current_exchanges)
    user.exchanges.add(*upcoming_exchanges)
    return user


@pytest.fixture
def other_upcoming_exchanges():
    """Other upcoming exchanges."""

    exchanges = []
    for i in range(2, 0, -1):
        exchanges.append(
            baker.make(
                models.Exchange,
                name=f"Other Upcoming Exchange {i}",
                slug=f"other-upcoming-exchange-{i}",
                drawn=now() + timedelta(days=i * 20),
                sent=now() + timedelta(days=i * 21),
                received=now() + timedelta(days=i * 22),
            )
        )

    return models.Exchange.objects.filter(id__in=[e.id for e in exchanges])
