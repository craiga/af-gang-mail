"""Views"""

from django import urls
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.views.generic import DeleteView, DetailView, TemplateView, UpdateView

from allauth.account.forms import SignupForm
from django_tables2.paginators import LazyPaginator
from django_tables2.views import SingleTableMixin, SingleTableView

from af_gang_mail import forms, models, tables, tasks



class Home(LoginRequiredMixin, TemplateView):
    """Home page for logged in users."""

    template_name = "af_gang_mail/home.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"user": self.request.user})
        return context_data


class UpdateNameAndAddress(LoginRequiredMixin, UpdateView):
    """Update name and address."""

    form_class = forms.UpdateNameAndAddress
    template_name = "af_gang_mail/update-name-and-address.html"

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        """Handle valid form."""

        response = super().form_valid(form)

        messages.success(
            self.request,
            self.get_success_message(),
            fail_silently=True,
        )

        return response

    def get_success_message(self):
        return f"Your name and/or address have been updated."

    def get_success_url(self):
        return urls.reverse("home")


class SelectExchanges(LoginRequiredMixin, UpdateView):
    """Select exchanges."""

    form_class = forms.SelectExchanges
    template_name = "af_gang_mail/select-exchanges.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["exchanges"] = context_data["form"].fields["exchanges"].queryset
        return context_data

    def form_valid(self, form):
        """Handle valid form."""

        response = super().form_valid(form)

        messages.success(
            self.request,
            self.get_success_message(),
            fail_silently=True,
        )

        return response

    def get_success_message(self):
        return "Your upcoming exchanges have been updated."

    def get_success_url(self):
        return urls.reverse("home")


class Landing(TemplateView):
    """Landing page."""

    template_name = "af_gang_mail/landing.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {"login_form": forms.LoginForm(), "register_form": SignupForm(),}
        )
        return context_data

    def get(self, request, *args, **kwargs):
        """If logged in user doesn't have name or address, redirect them to enter those details."""

        user = request.user
        if user.is_authenticated:
            return HttpResponseRedirect(urls.reverse("home"))

        return super().get(request, *args, **kwargs)


class SignUpStepOne(UpdateNameAndAddress):
    template_name = "af_gang_mail/sign-up/step-one.html"

    def get_success_message(self):
        return f"Thanks { self.request.user.get_full_name() }!"

    def get_success_url(self):
        return urls.reverse("sign-up-step-two")


class SignUpStepTwo(SelectExchanges):
    template_name = "af_gang_mail/sign-up/step-two.html"


class ManageExchanges(PermissionRequiredMixin, SingleTableView):
    """List exchanges."""

    permission_required = "af_gang_mail.view_exchange"
    model = models.Exchange
    template_name = "af_gang_mail/manage_exchanges/list.html"
    table_class = tables.Exchange
    paginator_class = LazyPaginator


class ViewExchange(PermissionRequiredMixin, SingleTableMixin, DetailView):
    """View exchange."""

    permission_required = "af_gang_mail.view_exchange"
    model = models.Exchange
    template_name = "af_gang_mail/manage_exchanges/view.html"
    context_object_name = "exchange"
    table_class = tables.User
    context_table_name = "user_table"
    paginator_class = LazyPaginator

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["exchange_data"] = model_to_dict(self.get_object())
        return context_data

    def get_table_data(self):
        return self.get_object().users.all()


class DeleteExchange(PermissionRequiredMixin, DeleteView):
    """Delete exchange."""

    permission_required = "af_gang_mail.delete_exchange"
    model = models.Exchange
    template_name = "af_gang_mail/manage_exchanges/delete.html"
    success_url = urls.reverse_lazy("manage-exchanges")


class DrawExchange(PermissionRequiredMixin, DetailView):
    """
    Manually run the draw for an exchange.

    This should only ever be used for testing the system.
    """

    permission_required = "af_gang_mail.add_draw"
    model = models.Exchange
    template_name = "af_gang_mail/manage_exchanges/draw.html"
    context_object_name = "exchange"

    def post(self, request, slug):  # pylint: disable=unused-argument
        """Start draw."""

        exchange = self.get_object()
        tasks.enqueue_draw_exchange_task(exchange)

        messages.info(
            self.request,
            f"Task to draw { exchange.name } has been submitted. Refresh this page to see results.",
            fail_silently=True,
        )

        return HttpResponseRedirect(urls.reverse("manage-exchanges"))


class StyleGallery(TemplateView):
    """Style gallery."""

    template_name = "af_gang_mail/style-gallery.html"

    def get(self, *args, **kwargs):
        for tag in ["debug", "info", "success", "warning", "error"]:
            write_message = getattr(messages, tag)
            write_message(self.request, f"Short { tag } message.")
            write_message(self.request, f"Another short { tag } message.")
            write_message(
                self.request,
                (
                    f"Quite an unnecessarily long { tag } message with lots of verbose waffling "
                    "detail about not much at all. In fact, you might suspect that it's "
                    "completely, 100 percent contrieved."
                ),
            )

        return super().get(*args, **kwargs)
