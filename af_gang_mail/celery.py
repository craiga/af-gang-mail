"""Celery initialization."""

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "af_gang_mail.settings")


# Start Celery
# https://docs.celeryproject.org/en/stable/django/

app = Celery("af_gang_mail")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
