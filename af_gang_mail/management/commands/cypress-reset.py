"""Reset the database for Cypress."""

# pylint: disable=invalid-name

import os
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.core.management.commands import flush, loaddata


class Command(flush.Command, loaddata.Command, BaseCommand):
    """Reset the database for Cypress."""

    help = __doc__

    def add_arguments(self, parser):
        """Set up arguments."""

        # Manually add the no-input argument from the flush command.
        # It's the only argument which isn't present in loaddata.
        # Calling add_arguments on both commands results in a argparse.ArgumentError.
        parser.add_argument(
            "--noinput",
            "--no-input",
            action="store_false",
            dest="interactive",
            help="Tells Django to NOT prompt the user for input of any kind.",
        )

        loaddata.Command.add_arguments(self, parser)

    def handle(self, *args, **kwargs):
        """Handle a call to the command."""

        flush.Command.handle(self, **kwargs)
        loaddata.Command.handle(self, *args, **kwargs)

        # Rename the example.com site.
        domain = "mail.afgang.co.uk"
        if "CYPRESS_BASE_URL" in os.environ:
            url = urlparse(os.environ["CYPRESS_BASE_URL"])
            domain = url.netloc
        elif settings.ALLOWED_HOSTS:
            domain = settings.ALLOWED_HOSTS[0]

        site = Site.objects.get(domain="example.com")
        site.name = "AF GANG Mail Exchange"
        site.domain = domain
        site.save()
