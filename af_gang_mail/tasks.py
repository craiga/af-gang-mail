"""Celery tasks."""

import logging

from django.conf import settings

from af_gang_mail import celery, models

logger = logging.getLogger(__name__)


def calculate_draw_exchange_time_limits(exchange, max_attempts=10):
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

    soft_time_limit = time_for_scoring

    if soft_time_limit < settings.CELERY_TASK_SOFT_TIME_LIMIT:
        logger.info(
            "Estimated time limit < configured time limit. Use configured time limit."
        )
        soft_time_limit = settings.CELERY_TASK_SOFT_TIME_LIMIT

    time_limit = (
        soft_time_limit
        + settings.CELERY_TASK_TIME_LIMIT
        - settings.CELERY_TASK_SOFT_TIME_LIMIT
    )

    return (soft_time_limit, time_limit)


@celery.app.task
def draw_exchange(exchange_id, max_attempts):
    """
    Draw an exchange.

    In local testing it took about 10 seconds to test for 10k users.
    """

    exchange = models.Exchange.objects.get(id=exchange_id)
    models.Draw.objects.bulk_create_from_exchange(exchange, max_attempts=max_attempts)
