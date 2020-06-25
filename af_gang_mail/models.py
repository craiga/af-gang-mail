"""Models."""

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now

from django_countries.fields import CountryField


class User(AbstractUser):
    """User"""

    address_line_1 = models.TextField("Address line 1", blank=True, null=False)
    address_line_2 = models.TextField("Address line 2", blank=True, null=False)
    address_city = models.TextField("City", blank=True, null=False)
    address_state = models.TextField("State", blank=True, null=False)
    address_postcode = models.TextField("Postcode", blank=True, null=False)
    address_country = CountryField("Country", blank=True, null=False)
    exchanges = models.ManyToManyField("Exchange")

    def __str__(self):
        """Full name or email address."""

        if self.get_full_name():
            return self.get_full_name()

        return self.email

    def get_full_address(self):
        """Get full address."""

        address_parts = [
            self.address_line_1,
            self.address_line_2,
            self.address_city,
            self.address_state,
            self.address_postcode,
            self.address_country.name,
        ]
        address_parts = [part for part in address_parts if part]
        return "\n".join(address_parts)

    def get_past_exchanges(self):
        return self.exchanges.filter(received__lt=now())

    def get_current_exchanges(self):
        return self.exchanges.filter(drawn__lte=now(), received__gte=now())

    def get_future_exchanges(self):
        return self.exchanges.filter(drawn__gt=now())


class Exchange(models.Model):
    """Exchange"""

    name = models.TextField(blank=False, null=False)
    drawn = models.DateTimeField(blank=False, null=False)
    sent = models.DateTimeField(blank=False, null=False)
    received = models.DateTimeField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def clean(self):
        if not self.drawn < self.sent < self.received:
            raise ValidationError(
                "Exchange must be drawn before it's sent and sent before it's recieved."
            )

        return super().clean()
