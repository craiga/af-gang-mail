"""AF GANG Mail"""

from af_gang_mail.celery import app as celery_app

__all__ = ["celery_app"]
