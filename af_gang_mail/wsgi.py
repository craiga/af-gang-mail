"""WSGI configuration for AF GANG Mail."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "af_gang_mail.settings")

application = get_wsgi_application()
