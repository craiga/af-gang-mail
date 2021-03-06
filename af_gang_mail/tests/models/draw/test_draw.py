"""Test drawing an exchange."""

# pylint: disable=redefined-outer-name

from django.db.utils import IntegrityError

import pytest
from allauth.account.models import EmailAddress
from model_bakery import baker

from af_gang_mail.models import Draw


@pytest.fixture
def exchange():
    return baker.make("af_gang_mail.Exchange", slug="my-cool-exchange")


@pytest.fixture
def users(exchange):
    """A number of confirmed users belonging to exchange."""

    users = []
    for _ in range(0, 5):
        user = baker.make(
            "af_gang_mail.User",
            emailaddress_set=baker.prepare(EmailAddress, verified=True, _quantity=1),
            _fill_optional=["first_name", "last_name"],
        )
        assert user.has_verified_email_address()
        user.exchanges.add(exchange, through_defaults={"confirmed": True})
        users.append(user)

    return users


@pytest.fixture
def unconfirmed_users(exchange):
    """A number of unconfirmed users belonging to exchange."""

    users = []
    for _ in range(0, 5):
        user = baker.make(
            "af_gang_mail.User",
            emailaddress_set=baker.prepare(EmailAddress, verified=True, _quantity=1),
            _fill_optional=["first_name", "last_name"],
        )
        assert user.has_verified_email_address()
        user.exchanges.add(exchange, through_defaults={"confirmed": False})
        users.append(user)

    return users


@pytest.mark.django_db
def test_draw(exchange, users, unconfirmed_users, django_assert_max_num_queries):
    """Test a simple draw."""
    # pylint: disable=unused-argument

    with django_assert_max_num_queries(2 + len(users)):
        draws = Draw.objects.bulk_create_from_exchange(exchange)

    assert len(draws) == len(users)

    for draw in draws:
        assert draw.sender != draw.recipient
        assert draw.sender in users
        assert draw.recipient in users


@pytest.mark.repeat(10)
@pytest.mark.django_db
def test_draw_with_past_exchange(exchange):
    """
    Test a small draw with a past exchange and one perfect solution.

    Featuring the Beastie Boys.
    """

    past_exchange = baker.make("af_gang_mail.Exchange", slug="past-exchange")

    # Set up the Beastie Boys.
    mike_d = baker.make(
        "af_gang_mail.User",
        username="mike_d",
        first_name="Michael",
        last_name="Diamond",
        emailaddress_set=baker.prepare(EmailAddress, verified=True, _quantity=1),
    )
    mike_d.exchanges.add(exchange, past_exchange, through_defaults={"confirmed": True})
    adrock = baker.make(
        "af_gang_mail.User",
        username="adrock",
        first_name="Adam",
        last_name="Horovitz",
        emailaddress_set=baker.prepare(EmailAddress, verified=True, _quantity=1),
    )
    adrock.exchanges.add(exchange, past_exchange, through_defaults={"confirmed": True})
    mca = baker.make(
        "af_gang_mail.User",
        username="mca",
        first_name="Adam",
        last_name="Yauch",
        emailaddress_set=baker.prepare(EmailAddress, verified=True, _quantity=1),
    )
    mca.exchanges.add(exchange, past_exchange, through_defaults={"confirmed": True})

    # Set up a previous draw.
    # Mike D => Adrock => MCA.
    baker.make(
        "af_gang_mail.Draw", sender=mike_d, recipient=adrock, exchange=past_exchange
    )
    baker.make(
        "af_gang_mail.Draw", sender=adrock, recipient=mca, exchange=past_exchange
    )
    baker.make(
        "af_gang_mail.Draw", sender=mca, recipient=mike_d, exchange=past_exchange
    )

    # Generate a new draw.
    draws = Draw.objects.bulk_create_from_exchange(exchange)

    # Test draws were generated as expected.
    assert len(draws) == exchange.users.count() == 3
    assert Draw.objects.filter(sender=mike_d, recipient=mca, exchange=exchange).exists()
    assert Draw.objects.filter(sender=mca, recipient=adrock, exchange=exchange).exists()
    assert Draw.objects.filter(
        sender=adrock, recipient=mike_d, exchange=exchange
    ).exists()


@pytest.mark.django_db
def test_impossible_draw(exchange):
    """
    Test an impossible draw will still give a solution.

    Featuring De La Soul.
    """

    past_exchange_1 = baker.make("af_gang_mail.Exchange", slug="past-exchange-1")
    past_exchange_2 = baker.make("af_gang_mail.Exchange", slug="past-exchange-2")

    # Set up De La Soul.
    posdnuos = baker.make(
        "af_gang_mail.User",
        username="posdnuos",
        first_name="Kelvin",
        last_name="Mercer",
        emailaddress_set=baker.prepare(EmailAddress, verified=True, _quantity=1),
    )
    posdnuos.exchanges.add(
        exchange, past_exchange_1, past_exchange_2, through_defaults={"confirmed": True}
    )
    trugoy = baker.make(
        "af_gang_mail.User",
        username="trugoy",
        first_name="David",
        last_name="Jolicoeur",
        emailaddress_set=baker.prepare(EmailAddress, verified=True, _quantity=1),
    )
    trugoy.exchanges.add(
        exchange, past_exchange_1, past_exchange_2, through_defaults={"confirmed": True}
    )
    maseo = baker.make(
        "af_gang_mail.User",
        username="maseo",
        first_name="Vincent",
        last_name="Mason",
        emailaddress_set=baker.prepare(EmailAddress, verified=True, _quantity=1),
    )
    maseo.exchanges.add(
        exchange, past_exchange_1, past_exchange_2, through_defaults={"confirmed": True}
    )

    # Set up first exchange.
    # Posdnous => Trugoy => Maseo.
    baker.make(
        "af_gang_mail.Draw", sender=posdnuos, recipient=trugoy, exchange=past_exchange_1
    )
    baker.make(
        "af_gang_mail.Draw", sender=trugoy, recipient=maseo, exchange=past_exchange_1
    )
    baker.make(
        "af_gang_mail.Draw", sender=maseo, recipient=posdnuos, exchange=past_exchange_1
    )

    # Set up second exchange.
    # Maseo => Trugoy => Posdnous.
    baker.make(
        "af_gang_mail.Draw", sender=maseo, recipient=trugoy, exchange=past_exchange_2
    )
    baker.make(
        "af_gang_mail.Draw", sender=trugoy, recipient=posdnuos, exchange=past_exchange_2
    )
    baker.make(
        "af_gang_mail.Draw", sender=posdnuos, recipient=maseo, exchange=past_exchange_2
    )

    # Generate a new draw.
    draws = Draw.objects.bulk_create_from_exchange(exchange, max_attempts=3)

    # Test draws were generated.
    assert len(draws) == exchange.users.count() == 3
    for draw in draws:
        assert draw.sender != draw.recipient
        assert draw.sender in [posdnuos, trugoy, maseo]
        assert draw.recipient in [posdnuos, trugoy, maseo]


@pytest.mark.django_db
def test_previous_conf_does_not_confirm(exchange):
    """
    Test confirmation of one exchange does not imply confirmation of another.

    Featuring Weezer.
    """

    past_exchange = baker.make("af_gang_mail.Exchange", slug="past-exchange")

    # Set up Weezer. Note that Matt Sharp hasn't confirmed for the current exchange.
    rivers = baker.make(
        "af_gang_mail.User",
        username="rivers",
        first_name="Rivers",
        last_name="Cuomo",
        emailaddress_set=baker.prepare(EmailAddress, verified=True, _quantity=1),
    )
    rivers.exchanges.add(exchange, past_exchange, through_defaults={"confirmed": True})
    pat = baker.make(
        "af_gang_mail.User",
        username="pat",
        first_name="Pat",
        last_name="Wilson",
        emailaddress_set=baker.prepare(EmailAddress, verified=True, _quantity=1),
    )
    pat.exchanges.add(exchange, past_exchange, through_defaults={"confirmed": True})
    brian = baker.make(
        "af_gang_mail.User",
        username="brian",
        first_name="Brian",
        last_name="Bell",
        emailaddress_set=baker.prepare(EmailAddress, verified=True, _quantity=1),
    )
    brian.exchanges.add(exchange, past_exchange, through_defaults={"confirmed": True})
    matt = baker.make(
        "af_gang_mail.User",
        username="matt",
        first_name="Matt",
        last_name="Sharp",
        emailaddress_set=baker.prepare(EmailAddress, verified=True, _quantity=1),
    )
    matt.exchanges.add(exchange, through_defaults={"confirmed": False})
    matt.exchanges.add(past_exchange, through_defaults={"confirmed": True})

    # Generate a new draw.
    draws = Draw.objects.bulk_create_from_exchange(exchange)

    # Test draws were generated.
    assert len(draws) == 3
    for draw in draws:
        assert draw.sender != draw.recipient
        assert draw.sender in [rivers, pat, brian]
        assert draw.recipient in [rivers, pat, brian]


@pytest.mark.django_db
def test_user_cannot_be_sender_twice(exchange, user):
    """Test that a user cannot be a sender twice for the same exchange."""

    baker.make("af_gang_mail.Draw", exchange=exchange, sender=user)
    with pytest.raises(IntegrityError):
        baker.make("af_gang_mail.Draw", exchange=exchange, sender=user)


@pytest.mark.django_db
def test_user_cannot_be_recipient_twice(exchange, user):
    """Test that a user cannot be a recipient twice for the same exchange."""

    baker.make("af_gang_mail.Draw", exchange=exchange, recipient=user)
    with pytest.raises(IntegrityError):
        baker.make("af_gang_mail.Draw", exchange=exchange, recipient=user)
