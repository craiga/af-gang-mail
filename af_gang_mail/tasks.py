"""Celery tasks."""

import logging

from django.conf import settings
from django.core import mail

from af_gang_mail import celery, models

logger = logging.getLogger(__name__)


def enqueue_draw_exchange_task(exchange):
    """Enqueue a draw_exchange task."""

    soft_time_limit, time_limit = _calculate_draw_exchange_time_limits(
        exchange, max_attempts=settings.CREATE_DRAW_MAX_ATTEMPTS
    )
    draw_exchange.apply_async(
        kwargs={
            "exchange_id": exchange.id,
            "max_attempts": settings.CREATE_DRAW_MAX_ATTEMPTS,
        },
        soft_time_limit=soft_time_limit,
        time_limit=time_limit,
    )


def _calculate_draw_exchange_time_limits(exchange, max_attempts=10):
    """Calculate the maximum amount of time we'd expect a draw to take."""

    num_users = exchange.users.count()

    logger.info("Calculating time for scoring a result for %d users.", num_users)
    soft_time_limit = num_users * settings.CREATE_DRAW_SECONDS_PER_USER
    logger.info("Estimated %f seconds to score %d users.", soft_time_limit, num_users)
    soft_time_limit = soft_time_limit * max_attempts
    logger.info(
        "Estimated %f seconds for %d users with up to %d attempts.",
        soft_time_limit,
        num_users,
        max_attempts,
    )

    if soft_time_limit < settings.CELERY_TASK_SOFT_TIME_LIMIT:
        logger.info(
            "Estimated time limit < configured time limit. Using configured time limit."
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

    To enqueue this task, call enqueue_draw_exchange_task which will set an appropriate
    time limit.
    """

    exchange = models.Exchange.objects.get(id=exchange_id)
    models.Draw.objects.bulk_create_from_exchange(exchange, max_attempts=max_attempts)

    if exchange.send_emails:
        send_draw_emails.delay(exchange.id)


@celery.app.task
def send_draw_emails(exchange_id):
    """Send emails for a draw."""

    exchange = models.Exchange.objects.get(id=exchange_id)
    connection = mail.get_connection()
    connection.send_messages([d.as_email_message() for d in exchange.draws.all()])
