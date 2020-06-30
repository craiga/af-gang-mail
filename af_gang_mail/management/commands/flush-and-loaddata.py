"""Flush the database and load fixtures in a single command."""

# pylint: disable=invalid-name

from django.core.management.base import BaseCommand
from django.core.management.commands import flush, loaddata


class Command(flush.Command, loaddata.Command, BaseCommand):
    """Flush the database and load fixtures in a single command."""

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
        flush.Command.handle(self, **kwargs)
        loaddata.Command.handle(self, *args, **kwargs)
