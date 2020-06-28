"""Celery tasks."""

from af_gang_mail import celery, models


@celery.app.task
def draw_exchange(exchange_id):
    """Draw an exchange."""

    exchange = models.Exchange.objects.get(id=exchange_id)
    models.Draw.objects.bulk_create_from_exchange(exchange)
