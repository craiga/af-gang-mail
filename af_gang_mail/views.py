"""Views"""

from django import urls
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.views.generic import DeleteView, DetailView, TemplateView, UpdateView

from csp.decorators import csp_exempt
from django_tables2.paginators import LazyPaginator
from django_tables2.views import MultiTableMixin, SingleTableView
from flatblocks import views as flatblocks_views

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
            self.request, self.get_success_message(), fail_silently=True,
        )

        return response

    def get_success_message(self):  # pylint: disable=no-self-use
        return "Your name and/or address have been updated."

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
            self.request, self.get_success_message(), fail_silently=True,
        )

        return response

    def get_success_message(self):  # pylint: disable=no-self-use
        return "Your upcoming exchanges have been updated."

    def get_success_url(self):
        return urls.reverse("home")


class Landing(TemplateView):
    """Landing page."""

    template_name = "af_gang_mail/landing.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {"login_form": forms.LoginForm(), "register_form": forms.SignupForm()}
        )
        return context_data

    def get(self, request, *args, **kwargs):
        """If logged in user doesn't have name or address, redirect them to enter those details."""

        user = request.user
        if user.is_authenticated:
            redirect_url = urls.reverse("home")
            if user.has_perm("flatblocks.change_flatblock"):
                messages.info(
                    self.request,
                    mark_safe(
                        "Normally you would be redirected to "
                        f"<a href='{ redirect_url }'>{ redirect_url }</a>, "
                        "but as you're logged in as a user with edit permissions you can stay "
                        "on this page to update it's content."
                    ),
                    fail_silently=True,
                )

            else:
                return HttpResponseRedirect(redirect_url)

        return super().get(request, *args, **kwargs)


class SignUpStepOne(UpdateNameAndAddress):
    """First step of sign up process."""

    template_name = "af_gang_mail/sign-up/step-one.html"

    def get_success_message(self):
        return f"Thanks { self.request.user.get_full_name() }!"

    def get_success_url(self):
        return urls.reverse("sign-up-step-two")


class SignUpStepTwo(SelectExchanges):
    """Second step of sign up process."""

    template_name = "af_gang_mail/sign-up/step-two.html"

    def get_success_message(self):
        return f"Thanks { self.request.user.get_full_name() }!"


class ManageExchanges(PermissionRequiredMixin, SingleTableView):
    """List exchanges."""

    permission_required = "af_gang_mail.view_exchange"
    model = models.Exchange
    template_name = "af_gang_mail/manage_exchanges/list.html"
    table_class = tables.Exchange
    paginator_class = LazyPaginator


class ViewExchange(PermissionRequiredMixin, MultiTableMixin, DetailView):
    """View exchange."""

    permission_required = "af_gang_mail.view_exchange"
    model = models.Exchange
    template_name = "af_gang_mail/manage_exchanges/view.html"
    context_object_name = "exchange"
    paginator_class = LazyPaginator

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["exchange_data"] = model_to_dict(self.get_object())
        context_data["user_table"] = context_data["tables"][0]
        context_data["draw_table"] = context_data["tables"][1]
        return context_data

    def get_tables(self):
        exchange = self.get_object()
        return [
            tables.User(exchange.users.all(), prefix="user-"),
            tables.Draw(exchange.draws.all(), prefix="draw-"),
        ]


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


class StyleGallery(PermissionRequiredMixin, TemplateView):
    """Style gallery."""

    template_name = "af_gang_mail/style-gallery.html"
    permission_required = "af_gang_mail.view_style_gallery"

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


class PageIndex(PermissionRequiredMixin, TemplateView):
    """Page index."""

    template_name = "af_gang_mail/page-index.html"
    permission_required = "flatblocks.change_flatblock"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["urls"] = []
        resolver = urls.get_resolver()
        for pattern in resolver.url_patterns:
            try:
                context_data["urls"].append(urls.reverse(pattern.name))
            except (AttributeError, urls.NoReverseMatch):
                pass

        return context_data


@csp_exempt
def edit_flatblock(request, pk, **kwargs):
    return flatblocks_views.edit(request, pk, modelform_class=forms.FlatBlock, **kwargs)


@login_required
def resend_verification(request):
    request.user.emailaddress_set.first().send_confirmation(request)
    messages.success(request, "A verification email is on its way!", fail_silently=True)
    return HttpResponseRedirect(urls.reverse("home"))
