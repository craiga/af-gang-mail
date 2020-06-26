"""Tables"""

import django_tables2 as tables

from af_gang_mail import models


class Exchange(tables.Table):
    """Exchange table."""

    class Meta:
        model = models.Exchange
        fields = ["name", "drawn", "sent", "received", "created", "modified"]
