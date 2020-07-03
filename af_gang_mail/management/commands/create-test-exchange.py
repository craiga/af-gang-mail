"""Create a test exchange."""

# pylint: disable=invalid-name

import logging
import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction

import factory
import faker
from allauth.account.models import EmailAddress
from dateutil.parser import parse

from af_gang_mail import models

logger = logging.getLogger(__name__)


def parsed_datetime_string(in_value):
    return parse(in_value, fuzzy=True)


class ExchangeFactory(factory.django.DjangoModelFactory):
    """Fake exchange factory."""

    name = factory.Faker("word")
    drawn = factory.Faker("date_time")
    sent = factory.LazyAttribute(lambda self: self.drawn + timedelta(days=7))
    received = factory.LazyAttribute(lambda self: self.sent + timedelta(days=7))

    class Meta:
        model = models.Exchange


class EmailAddressFactory(factory.django.DjangoModelFactory):
    """Email address factory."""

    email = factory.Faker("email")

    class Meta:
        model = EmailAddress


class UserFactory(factory.django.DjangoModelFactory):
    """Fake user factory."""

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    emailaddress = factory.RelatedFactory(
        EmailAddressFactory, factory_related_name="user", verified=True
    )

    class Meta:
        model = models.User


class Command(BaseCommand):
    """Create a test exchange."""

    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument(
            "--name", help="Name of the exchange.",
        )
        parser.add_argument(
            "--drawn",
            type=parsed_datetime_string,
            help="When the exchange will be drawn.",
        )
        parser.add_argument(
            "--sent",
            type=parsed_datetime_string,
            help="When the exchange will be sent.",
        )
        parser.add_argument(
            "--received",
            type=parsed_datetime_string,
            help="When the exchange will be received.",
        )
        parser.add_argument(
            "--num-users",
            type=int,
            default=1000,
            help="How many users are part of the draw.",
        )
        parser.add_argument(
            "--reuse-users",
            action="store_true",
            help="Reuse existing users. Don't create new users.",
        )
        parser.add_argument(
            "--created-user-last-name", help="The last name to give any created users.",
        )

    def _create_exchange(self, options):  # pylint: disable=no-self-use
        """Create fake exchange."""

        exchange_field_names = [field.name for field in models.Exchange._meta.fields]
        exchange_kwargs = {
            key: options[key] for key in options if key in exchange_field_names
        }
        exchange = ExchangeFactory(**exchange_kwargs)
        exchange.full_clean()
        return exchange

    def _create_users(self, options):  # pylint: disable=no-self-use
        """Create fake users."""

        if options["reuse_users"]:
            all_user_ids = list(models.User.objects.values_list("id", flat=True))
            if len(all_user_ids) < options["num_users"]:
                raise RuntimeError("There aren't enough existing users to reuse.")

            random.shuffle(all_user_ids)
            return models.User.objects.filter(
                id__in=all_user_ids[0 : options["num_users"]]
            )

        user_kwargs = {}
        for key, value in options.items():
            if key.startswith("created-user-"):
                user_kwargs[key[13:]] = value

        users = []
        fake = faker.Faker()
        for _ in range(0, options["num_users"]):
            username = fake.user_name()
            while models.User.objects.filter(
                username=username
            ).exists() or username in [u.username for u in users]:
                username = fake.user_name()

            users.append(UserFactory(username=username, **user_kwargs))

        return users

    @transaction.atomic()
    def handle(self, *args, **options):
        """Handle a call to the command."""
        # Set logging level.
        # 0 = minimal output, 1 = normal output, 2 = verbose output, and
        # 3 = very verbose output.
        log_levels = (logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG)
        logger.setLevel(log_levels[options["verbosity"]])

        # Remove options with none values.
        options = {key: options[key] for key in options if options[key] is not None}

        exchange = self._create_exchange(options)
        for user in self._create_users(options):
            user.exchanges.add(exchange)
