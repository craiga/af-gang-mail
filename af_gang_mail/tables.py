"""Tables"""

import django_tables2 as tables
from django_tables2 import columns
from django_tables2.utils import A

from af_gang_mail import models


class Exchange(tables.Table):
    """Exchange table."""

    name = columns.LinkColumn(viewname="view-exchange", kwargs={"slug": A("slug")},)

    delete = columns.LinkColumn(
        viewname="delete-exchange",
        kwargs={"slug": A("slug")},
        text="Delete",
        orderable=False,
    )

    class Meta:
        model = models.Exchange
        fields = [
            "name",
            "user_count",
            "drawn",
            "sent",
            "received",
            "created",
            "updated",
            "delete",
        ]

    def before_render(self, request):
        """Hide columns based on user permission."""

        if not request.user.has_perm("af_gang_mail.delete_exchange"):
            self.columns.hide("delete")

        return super().before_render(request)


class User(tables.Table):
    """User table."""

    class Meta:
        model = models.User
        fields = [
            "first_name",
            "last_name",
            "email",
        ]
