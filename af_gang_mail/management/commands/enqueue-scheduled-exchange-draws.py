"""Enqueue scheduled exchange draws."""

# pylint: disable=invalid-name

import logging

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from af_gang_mail import models, tasks

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Enqueue scheduled exchange draws."""

    help = __doc__

    def handle(self, *args, **options):
        """Handle a call to the command."""
        # Set logging level.
        # 0 = minimal output, 1 = normal output, 2 = verbose output, and
        # 3 = very verbose output.
        log_levels = (logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG)
        logger.setLevel(log_levels[options["verbosity"]])

        logger.info("Starting.")
        for exchange in models.Exchange.objects.scheduled_for_draw():
            logger.info("Enqueueing draw for %s.", exchange.name)
            exchange.draw_started = now()
            exchange.save()
            logger.debug(
                "Set draw_started for %s to %s.", exchange.name, exchange.draw_started
            )
            tasks.enqueue_draw_exchange_task(exchange)
            logger.info("Enqueued draw for %s.", exchange.name)

        logger.info("Done.")
