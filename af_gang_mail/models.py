"""Models."""

import logging
import random

from django import template, urls
from django.conf import settings
from django.contrib import auth
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models import Q
from django.utils.timezone import now

from autoslug import AutoSlugField
from django_countries.fields import CountryField

logger = logging.getLogger(__name__)


class UserManager(auth.models.UserManager):
    """User manager."""

    def eligible_for_draw(self):
        return self.filter(emailaddress__verified=True).exclude(
            Q(first_name="") & Q(last_name="")
        )


class User(auth.models.AbstractUser):
    """User"""

    street_address = models.TextField("Street Address", blank=True, null=False)
    address_city = models.TextField("City", blank=True, null=False)
    address_state = models.TextField("State", blank=True, null=False)
    address_postcode = models.TextField("Postcode", blank=True, null=False)
    address_country = CountryField("Country", blank=True, null=False)
    exchanges = models.ManyToManyField("Exchange", related_name="users")

    objects = UserManager()

    def __str__(self):
        """Full name or email address."""

        if self.get_full_name():
            return self.get_full_name()

        if self.email:
            return self.email

        return super().__str__()

    def get_address_parts(self):
        """Get the parts of the address."""

        address_parts = [
            self.street_address,
            self.address_city,
            self.address_state,
            self.address_postcode,
            self.address_country.name,
        ]
        return [part for part in address_parts if part]

    def get_full_address(self):
        return "\n".join(self.get_address_parts())

    def has_short_address(self):
        return len(self.get_address_parts()) < 3

    def has_verified_email_address(self):
        return self.emailaddress_set.filter(verified=True).exists()

    class Meta:
        permissions = [
            ("statto", "Can view statto"),
        ]


class ExchangeManager(models.Manager):
    """Exchange manager."""

    def upcoming(self):
        return self.filter(drawn__gt=now())

    def not_upcoming(self):
        return self.filter(drawn__lt=now())

    def scheduled_for_draw(self):
        return self.filter(drawn__lt=now(), draw_started__isnull=True)

    def drawn_not_sent(self):
        return self.filter(drawn__lt=now(), sent__gt=now())

    def past(self):
        return self.filter(received__lt=now())


class Exchange(models.Model):
    """Exchange"""

    name = models.TextField(blank=False, null=False)
    slug = AutoSlugField(populate_from="name", unique=True)
    drawn = models.DateTimeField(blank=False, null=False)
    sent = models.DateTimeField(blank=False, null=False)
    received = models.DateTimeField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    draw_started = models.DateTimeField(blank=True, null=True)
    send_emails = models.BooleanField(default=False)

    objects = ExchangeManager()

    def __str__(self):
        return self.name

    def clean(self):
        if not self.drawn < self.sent < self.received:
            raise ValidationError(
                "Exchange must be drawn before it's sent and sent before it's recieved."
            )

        return super().clean()


class DrawManager(models.Manager):
    """Draw manager."""

    def _user_pairs(self, users):  # pylint: disable=no-self-use
        for i in range(-1, len(users) - 1):
            yield (users[i], users[i + 1])

    def _draws(self, exchange, users):
        for sender, recipient in self._user_pairs(users):
            yield Draw(sender=sender, recipient=recipient, exchange=exchange)

    def _score_draws(self, draws):
        """
        Score a set of draws.

        The lower the score, the better.

        Zero is a perfect score.
        """

        # Count number of repeated sender/recipient pairs
        logger.info("Testing for %d repeated sender-recipient pairs.", len(draws))
        repeated_sender_recipient_pairs = 0
        for i, draw in enumerate(draws):
            if self.filter(
                sender_id=draw.sender_id, recipient_id=draw.recipient_id
            ).exists():
                repeated_sender_recipient_pairs = repeated_sender_recipient_pairs + 1

            if i % 1000 == 0 and i > 0:
                logger.info("Tested %d/%d sender-recipient pairs.", i, len(draws))

        logger.info(
            "Got %d repeated sender-recipient pairs.", repeated_sender_recipient_pairs
        )

        return repeated_sender_recipient_pairs

    def bulk_create_from_exchange(self, exchange, max_attempts=1000):
        """Create draws for an exchange."""

        logger.info("Preparing set of draws for %s.", exchange.name)

        users = list(exchange.users.eligible_for_draw())
        logger.info("%d users.", len(users))

        # Run through some iterations and try to generate a perfect result.
        iteration_results = []
        while len(iteration_results) < max_attempts:
            logger.info("Shuffling users.")
            random.shuffle(users)
            logger.info("Shuffled users.")

            logger.info("Generating draws.")
            draws = list(self._draws(exchange, users))
            logger.info("Generated draws.")

            logger.info("Scoring draws.")
            score = self._score_draws(draws)
            logger.info("Draws scored %d (higher is worse; zero is perfect).", score)
            if score == 0:
                logger.info("Got a perfect result!")
                break

            iteration_results.append((score, draws))

        if score > 0:
            logger.info("Didn't get a perfect result. Selecting the best result.")
            result = min(iteration_results, key=lambda result: result[0])
            logger.info(
                "Selected a result with score %d (higher is worse; zero is perfect).",
                result[0],
            )
            draws = result[1]

        logger.info("Writing draws to database.")
        return self.bulk_create(draws)


class Draw(models.Model):
    """Draw of a sender and a recipient for an exchange."""

    sender = models.ForeignKey(
        "af_gang_mail.User", on_delete=models.PROTECT, related_name="draws_as_sender"
    )
    recipient = models.ForeignKey(
        "af_gang_mail.User", on_delete=models.PROTECT, related_name="draws_as_recipient"
    )
    exchange = models.ForeignKey(
        "af_gang_mail.Exchange", on_delete=models.PROTECT, related_name="draws"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = DrawManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["exchange", "sender"], name="send_once_per_exchange"
            ),
            models.UniqueConstraint(
                fields=["exchange", "recipient"], name="receive_once_per_exchange"
            ),
        ]

    def as_email_message(self, **kwargs):
        """Construct an EmailMessage for this draw."""

        subject_template = template.loader.get_template(
            "af_gang_mail/draw-email-subject.txt"
        )
        body_text_template = template.loader.get_template(
            "af_gang_mail/draw-email-body.txt"
        )
        body_html_template = template.loader.get_template(
            "af_gang_mail/draw-email-body.html"
        )

        site = Site.objects.get_current()
        scheme = "https" if settings.SECURE_SSL_REDIRECT else "http"
        exchange_url = f"{ scheme }://{ site.domain }" + urls.reverse(
            "draw", kwargs={"slug": self.exchange.slug}
        )
        context = {"draw": self, "site": site, "exchange_url": exchange_url}

        msg = EmailMultiAlternatives(
            subject=subject_template.render(context),
            body=body_text_template.render(context),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[self.sender.email],
            **kwargs,
        )
        msg.attach_alternative(body_html_template.render(context), "text/html")

        return msg
