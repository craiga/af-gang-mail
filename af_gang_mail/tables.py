"""Tables"""

from django.contrib import flatpages

import django_tables2 as tables
from django_tables2 import columns
from django_tables2.utils import A

from af_gang_mail import models


class Exchange(tables.Table):
    """Exchange table."""

    name = columns.LinkColumn(viewname="view-exchange", kwargs={"slug": A("slug")},)
    users = tables.Column(verbose_name="Users")

    class Meta:
        model = models.Exchange
        fields = [
            "name",
            "users",
            "send_emails",
            "drawn",
            "sent",
            "received",
            "created",
            "updated",
            "draw_started",
        ]

    def render_users(self, value):  # pylint: disable=no-self-use
        return value.count()


class User(tables.Table):
    """User table."""

    class Meta:
        model = models.User
        fields = [
            "first_name",
            "last_name",
            "email",
        ]


class Draw(tables.Table):
    """Draw table."""

    sender = columns.LinkColumn(viewname="view-draw", kwargs={"pk": A("id")},)
    recipient = columns.LinkColumn(viewname="view-draw", kwargs={"pk": A("id")},)

    class Meta:
        model = models.Draw
        fields = [
            "sender",
            "recipient",
        ]


class FlatPage(tables.Table):
    """Flat page table."""

    title = columns.LinkColumn(viewname="update-flatpage", kwargs={"pk": A("id")},)

    class Meta:
        model = flatpages.models.FlatPage
        fields = [
            "title",
            "url",
        ]
