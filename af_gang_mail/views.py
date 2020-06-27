"""Views"""

from django import urls
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.views.generic import DeleteView, DetailView, TemplateView, UpdateView

from allauth.account.forms import LoginForm, SignupForm
from django_tables2.views import SingleTableMixin, SingleTableView

from af_gang_mail import forms, models, tables


class Home(TemplateView):
    """Home page."""

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context_data.update({"user": self.request.user})

        else:
            context_data.update(
                {"login_form": LoginForm(), "register_form": SignupForm(),}
            )

        return context_data

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ["af_gang_mail/home/authenticated.html"]

        return ["af_gang_mail/home/unauthenticated.html"]

    def get(self, request, *args, **kwargs):
        """If logged in user doesn't have name or address, redirect them to enter those details."""

        user = request.user
        if user.is_authenticated:
            if not user.get_full_name() or not user.get_full_address():
                return HttpResponseRedirect(urls.reverse("update-name-and-address"))

            if not user.exchanges.exists():
                return HttpResponseRedirect(urls.reverse("select-exchanges"))

        return super().get(request, *args, **kwargs)


class UpdateNameAndAddress(LoginRequiredMixin, UpdateView):
    """Update name and address."""

    form_class = forms.UpdateNameAndAddress
    template_name = "af_gang_mail/update_name_and_address.html"

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        """Handle valid form."""

        response = super().form_valid(form)

        messages.success(
            self.request,
            f"Thanks { self.request.user.get_full_name() }!",
            fail_silently=True,
        )

        return response

    def get_success_url(self):
        return urls.reverse("home")


class SelectExchanges(LoginRequiredMixin, UpdateView):
    """Select exchanges."""

    form_class = forms.SelectExchanges
    template_name = "af_gang_mail/select_exchanges.html"

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        """Handle valid form."""

        response = super().form_valid(form)

        messages.success(
            self.request,
            f"Thanks { self.request.user.get_full_name() }!",
            fail_silently=True,
        )

        return response

    def get_success_url(self):
        return urls.reverse("home")


class ManageExchanges(PermissionRequiredMixin, SingleTableView):
    """List exchanges."""

    permission_required = "af_gang_mail.view_exchange"
    model = models.Exchange
    template_name = "af_gang_mail/manage_exchanges/list.html"
    table_class = tables.Exchange

    def get_table_data(self):
        return super().get_table_data().annotate(user_count=Count("users"))


class ViewExchange(PermissionRequiredMixin, SingleTableMixin, DetailView):
    """View exchange."""

    permission_required = "af_gang_mail.view_exchange"
    model = models.Exchange
    template_name = "af_gang_mail/manage_exchanges/view.html"
    context_object_name = "exchange"
    table_class = tables.User
    context_table_name = "user_table"

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
