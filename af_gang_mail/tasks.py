"""Celery tasks."""

import logging

from af_gang_mail import celery, models

logger = logging.getLogger(__name__)


def calculate_draw_exchange_time_limit(exchange, max_attempts=10):
    """
    Calculate the maximum amount of time we'd expect a draw to take.

    In local testing it took about 10 seconds to test for 10k users.
    """
    num_users = exchange.users.count()

    logger.info("Calculating time for scoring a result for %d users.", num_users)
    time_for_scoring = num_users / 1000
    logger.info("Estimated %f seconds to score %d users.", time_for_scoring, num_users)
    time_for_scoring = time_for_scoring * max_attempts
    logger.info(
        "Estimated %f seconds to score %d users up to %d times.",
        time_for_scoring,
        num_users,
        max_attempts,
    )

    return time_for_scoring


@celery.app.task
def draw_exchange(exchange_id, max_attempts):
    """
    Draw an exchange.

    In local testing it took about 10 seconds to test for 10k users.
    """

    exchange = models.Exchange.objects.get(id=exchange_id)
    models.Draw.objects.bulk_create_from_exchange(exchange, max_attempts=max_attempts)
