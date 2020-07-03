"""Tables"""

import django_tables2 as tables
from django_tables2 import columns
from django_tables2.utils import A

from af_gang_mail import models


class Exchange(tables.Table):
    """Exchange table."""

    name = columns.LinkColumn(viewname="view-exchange", kwargs={"slug": A("slug")},)
    users = tables.Column(verbose_name="Users")
    draws = tables.Column(verbose_name="Draws")
    delete = columns.LinkColumn(
        viewname="delete-exchange",
        kwargs={"slug": A("slug")},
        text="Delete",
        orderable=False,
    )
    draw = columns.LinkColumn(
        viewname="draw-exchange",
        kwargs={"slug": A("slug")},
        text="Draw",
        orderable=False,
    )

    class Meta:
        model = models.Exchange
        fields = [
            "name",
            "users",
            "draws",
            "drawn",
            "sent",
            "received",
            "created",
            "updated",
            "delete",
            "draw",
        ]

    def before_render(self, request):
        """Hide columns based on user permission."""

        if not request.user.has_perm("af_gang_mail.delete_exchange"):
            self.columns.hide("delete")

        return super().before_render(request)

    def render_users(self, value):  # pylint: disable=no-self-use
        return value.count()

    def render_draws(self, value):  # pylint: disable=no-self-use
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

    class Meta:
        model = models.Draw
        fields = [
            "sender",
            "recipient",
        ]
