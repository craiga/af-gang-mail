"""Models."""

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User"""

    def __str__(self):
        """Full name or email address."""

        if self.get_full_name():
            return self.get_full_name()

        return self.email
