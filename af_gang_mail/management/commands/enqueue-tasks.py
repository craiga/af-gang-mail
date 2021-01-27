"""Enqueue tasks."""

# pylint: disable=invalid-name

import logging

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from af_gang_mail import models, tasks

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Enqueue tasks."""

    help = __doc__

    def handle(self, *args, **options):
        """Handle a call to the command."""
        # Set logging level.
        # 0 = minimal output, 1 = normal output, 2 = verbose output, and
        # 3 = very verbose output.
        log_levels = (logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG)
        logger.setLevel(log_levels[options["verbosity"]])

        logger.info("Starting.")

        logger.info("Looking for confirmation messages to send…")
        for exchange in models.Exchange.objects.scheduled_for_confirmation():
            logger.info("Enqueueing confirmation messages for %s.", exchange.name)
            exchange.confirmation_started = now()
            exchange.save()
            logger.debug(
                "Set confirmation_started for %s to %s.",
                exchange.name,
                exchange.confirmation_started,
            )
            tasks.send_confirmation_emails.delay(exchange.id)
            logger.info("Enqueued confirmation messages for %s.", exchange.name)

        logger.info("Looking for confirmation reminder messages to send…")
        for exchange in models.Exchange.objects.scheduled_for_confirmation_reminder():
            logger.info(
                "Enqueueing confirmation reminder messages for %s.", exchange.name
            )
            exchange.confirmation_reminder_started = now()
            exchange.save()
            logger.debug(
                "Set confirmation_reminder_started for %s to %s.",
                exchange.name,
                exchange.confirmation_reminder_started,
            )
            tasks.send_confirmation_reminder_emails.delay(exchange.id)
            logger.info(
                "Enqueued confirmation reminder messages for %s.", exchange.name
            )

        logger.info("Looking for exchanges to draw…")
        for exchange in models.Exchange.objects.scheduled_for_draw():
            logger.info("Enqueueing draw for %s.", exchange.name)
            exchange.draw_started = now()
            exchange.save()
            logger.debug(
                "Set draw_started for %s to %s.", exchange.name, exchange.draw_started
            )
            tasks.enqueue_draw_exchange_task(exchange)
            logger.info("Enqueued draw for %s.", exchange.name)

        logger.info("Looking for exchanges for send reminders…")
        for exchange in models.Exchange.objects.scheduled_for_send_reminder():
            logger.info("Enqueueing send reminder for %s.", exchange.name)
            exchange.send_reminder_started = now()
            exchange.save()
            logger.debug(
                "Set send_reminder_started for %s to %s.",
                exchange.name,
                exchange.send_reminder_started,
            )
            tasks.send_send_reminders.delay(exchange.id)
            logger.info("Enqueued send reminder for %s.", exchange.name)

        logger.info("Looking for exchanges for receive reminders…")
        for exchange in models.Exchange.objects.scheduled_for_receive_reminder():
            logger.info("Enqueueing receive reminder for %s.", exchange.name)
            exchange.receive_reminder_started = now()
            exchange.save()
            logger.debug(
                "Set receive_reminder_started for %s to %s.",
                exchange.name,
                exchange.receive_reminder_started,
            )
            tasks.send_receive_reminders.delay(exchange.id)
            logger.info("Enqueued receive reminder for %s.", exchange.name)

        logger.info("Done.")
