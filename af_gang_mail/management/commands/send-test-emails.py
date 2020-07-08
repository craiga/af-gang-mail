"""Send test emails."""

# pylint: disable=invalid-name

from time import sleep

from django.core.mail import send_mail
from django.core.management.base import BaseCommand

import faker
from tqdm import tqdm

fake = faker.Faker()


class Command(BaseCommand):
    """Send test emails."""

    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument(
            "--num-emails", type=int, help="Number of emails to send.", default=1,
        )
        parser.add_argument(
            "--recipient", help="Recipient email address.",
        )
        parser.add_argument(
            "--from-email", help="Sender email address.",
        )
        parser.add_argument(
            "--subject", help="Email subject.",
        )
        parser.add_argument(
            "--message", help="Email body.",
        )
        parser.add_argument(
            "--pause", help="Seconds to pause between sending.", default=0, type=int,
        )

    def _send_mail(
        self, subject=None, message=None, from_email=None, recipient=None, **_
    ):  # pylint: disable=no-self-use
        """Send mail."""

        if not subject:
            subject = fake.sentence()

        if not message:
            message = "\n\n".join(fake.paragraphs())

        if not from_email:
            from_email = fake.email()

        if not recipient:
            recipient = fake.email()

        return send_mail(subject, message, from_email, [recipient])

    def handle(self, *args, **options):
        """Handle a call to the command."""

        for _ in tqdm(
            range(0, options["num_emails"]), desc="Sending emails", unit="emails"
        ):
            self._send_mail(**options)
            sleep(options["pause"])
