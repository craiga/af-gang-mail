"""Models."""

from django.contrib.auth.models import AbstractUser
from django.db import models

from django_countries.fields import CountryField


class User(AbstractUser):
    """User"""

    address_line_1 = models.TextField("Address line 1", blank=True, null=False)
    address_line_2 = models.TextField("Address line 2", blank=True, null=False)
    address_city = models.TextField("City", blank=True, null=False)
    address_state = models.TextField("State", blank=True, null=False)
    address_postcode = models.TextField("Postcode", blank=True, null=False)
    address_country = CountryField("Country", blank=True, null=False)

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
