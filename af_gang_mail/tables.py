"""Tables"""

import django_tables2 as tables
from django_tables2 import columns
from django_tables2.utils import A

from af_gang_mail import models


class Exchange(tables.Table):
    """Exchange table."""

    delete = columns.LinkColumn(
        viewname="delete-exchange", kwargs={"slug": A("slug")}, text="Delete"
    )

    class Meta:
        model = models.Exchange
        fields = ["name", "drawn", "sent", "received", "created", "modified", "delete"]

    def before_render(self, request):
        """Hide columns based on user permission."""

        if not request.user.has_perm("af_gang_mail.delete_exchange"):
            self.columns.hide("delete")

        return super().before_render(request)
