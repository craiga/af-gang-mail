"""Views"""

from math import floor

from django import http, template, urls
from django.conf import settings
from django.contrib import flatpages, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.sites.models import Site
from django.core import mail
from django.db.models import Q
from django.forms.models import model_to_dict
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    TemplateView,
    UpdateView,
)

import django_countries
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

        user = self.request.user
        active_draws = []
        for exchange in user.exchanges.drawn_not_sent():
            try:
                draw = user.draws_as_sender.get(exchange=exchange)
                active_draws.append((exchange, draw.recipient))
            except models.Draw.DoesNotExist:
                pass

        upcoming_exchanges = []
        user_upcoming_exchanges = user.exchanges.all()
        for exchange in models.Exchange.objects.upcoming():
            upcoming_exchanges.append((exchange in user_upcoming_exchanges, exchange))

        user_eligible_for_draws = (
            user.has_verified_email_address() and not user.get_full_name()
        )

        context_data.update(
            {
                "user": user,
                "active_draws": active_draws,
                "upcoming_exchanges": upcoming_exchanges,
                "user_eligible_for_draws": user_eligible_for_draws,
            }
        )

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


class Draw(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    View details of a draw for the logged in user.
    """

    model = models.Exchange
    template_name = "af_gang_mail/draw.html"
    context_object_name = "exchange"

    def has_permission(self):
        return models.Draw.objects.filter(
            exchange=self.get_object(), sender=self.request.user
        ).exists()

    def get_draw(self):
        return models.Draw.objects.get(
            exchange=self.get_object(), sender=self.request.user
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        draw = self.get_draw()
        context_data.update(draw.get_context_data())
        return context_data


class MailSent(FormView, Draw):
    """Mark draw as sent."""

    form_class = forms.MailSent
    template_name = "af_gang_mail/draw-sent.html"

    def form_valid(self, form):
        draw = self.get_draw()

        connection = mail.get_connection()
        connection.send_messages(
            [self.create_email_message(draw, form["message"].value)]
        )

        draw.sent = timezone.now()
        draw.save()

        messages.success(
            self.request,
            (
                f"Thanks! We've let { draw.recipient.get_full_name() } know that mail "
                "is on its way!"
            ),
            fail_silently=True,
        )

        return super().form_valid(form)

    def create_email_message(self, draw, message):  # pylint: disable=no-self-use
        """Create email message."""

        subject_template = template.loader.get_template(
            "af_gang_mail/mail-sent-subject.txt"
        )
        body_text_template = template.loader.get_template(
            "af_gang_mail/mail-sent-body.txt"
        )
        body_html_template = template.loader.get_template(
            "af_gang_mail/mail-sent-body.html"
        )

        site = Site.objects.get_current()
        scheme = "https" if settings.SECURE_SSL_REDIRECT else "http"
        exchange_url = f"{ scheme }://{ site.domain }" + urls.reverse(
            "draw", kwargs={"slug": draw.exchange.slug}
        )

        context = {
            "message": message,
            "exchange": draw.exchange,
            "sender": draw.sender,
            "recipient": draw.recipient,
            "site": site,
            "exchange_url": exchange_url,
        }

        msg = mail.EmailMultiAlternatives(
            subject=subject_template.render(context),
            body=body_text_template.render(context),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[draw.recipient.email],
        )
        msg.attach_alternative(body_html_template.render(context), "text/html")
        return msg

    def get_success_url(self):
        return urls.reverse("draw", kwargs={"slug": self.get_draw().exchange.slug})


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
        """If user is logged in, redirect them to home."""

        user = request.user
        if user.is_authenticated:
            redirect_url = urls.reverse("home")
            if user.has_perm("flatblocks.change_flatblock"):
                messages.info(
                    self.request,
                    mark_safe(
                        "Normally you would be redirected to "
                        f"<a href='{ redirect_url }'>{ redirect_url }</a>, "
                        "but as you're logged in as a user with edit permissions you "
                        "can stay on this page to update it's content."
                    ),
                    fail_silently=True,
                )

            else:
                return http.HttpResponseRedirect(redirect_url)

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
        sign_up_success_template = template.loader.get_template(
            "af_gang_mail/sign-up-success-message.txt"
        )
        return sign_up_success_template.render(
            {"name": self.request.user.get_full_name()}
        )


class ManageExchanges(LoginRequiredMixin, PermissionRequiredMixin, SingleTableView):
    """List exchanges."""

    permission_required = "af_gang_mail.view_exchange"
    model = models.Exchange
    template_name = "af_gang_mail/manage_exchanges/list.html"
    table_class = tables.Exchange
    paginator_class = LazyPaginator


class ViewExchange(
    LoginRequiredMixin, PermissionRequiredMixin, MultiTableMixin, DetailView
):
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


class CreateExchange(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Create exchange."""

    permission_required = "af_gang_mail.add_exchange"
    model = models.Exchange
    template_name = "af_gang_mail/manage_exchanges/create.html"
    form_class = forms.Exchange

    def get_success_url(self):
        return urls.reverse("view-exchange", kwargs={"slug": self.object.slug})


class UpdateExchange(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Modify exchange."""

    permission_required = "af_gang_mail.change_exchange"
    model = models.Exchange
    template_name = "af_gang_mail/manage_exchanges/update.html"
    form_class = forms.Exchange

    def get_success_url(self):
        return urls.reverse("view-exchange", kwargs={"slug": self.get_object().slug})


class DeleteExchange(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Delete exchange."""

    permission_required = "af_gang_mail.delete_exchange"
    model = models.Exchange
    template_name = "af_gang_mail/manage_exchanges/delete.html"
    success_url = urls.reverse_lazy("manage-exchanges")


class DrawExchange(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
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
            f"Task to draw { exchange.name } has been submitted. "
            "Refresh this page to see results.",
            fail_silently=True,
        )

        return http.HttpResponseRedirect(
            urls.reverse("view-exchange", kwargs={"slug": exchange.slug})
        )


class DeleteDrawsForExchange(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Delete existing draws for an exchange."""

    permission_required = "af_gang_mail.delete_draw"
    model = models.Exchange
    template_name = "af_gang_mail/manage_exchanges/delete-draws-for-exchange.html"
    context_object_name = "exchange"

    def post(self, request, slug):  # pylint: disable=unused-argument
        """Delete draws."""

        exchange = self.get_object()
        exchange.draws.all().delete()

        messages.info(
            self.request, f"Draws for { exchange.name } deleted.", fail_silently=True,
        )

        return http.HttpResponseRedirect(
            urls.reverse("view-exchange", kwargs={"slug": exchange.slug})
        )


class ViewDraw(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """View draw."""

    permission_required = "af_gang_mail.view_draw"
    model = models.Draw
    template_name = "af_gang_mail/manage_exchanges/view-draw.html"
    context_object_name = "draw"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["draw_data"] = model_to_dict(self.get_object())
        context_data[
            "draw_email_message"
        ] = self.get_object().as_created_email_message()
        return context_data


class StyleGallery(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
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
                    f"Quite an unnecessarily long { tag } message with lots of verbose "
                    "waffling detail about not much at all. In fact, you might suspect "
                    "that it's completely, 100 percent contrieved."
                ),
            )

        return super().get(*args, **kwargs)


class PageIndex(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
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


class Statto(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Statto page."""

    template_name = "af_gang_mail/statto.html"
    permission_required = "af_gang_mail.statto"

    def _get_user_percentages(self):  # pylint: disable=no-self-use
        """User percentages."""

        users = models.User.objects.count()
        user_stats = {
            "Users with Verified Email": models.User.objects.filter(
                emailaddress__verified=True
            ).count(),
            "Users with First Name": models.User.objects.exclude(first_name="").count(),
            "Users with Last Name": models.User.objects.exclude(last_name="").count(),
            "Users with Address Line 1": models.User.objects.exclude(
                address_line_1=""
            ).count(),
            "Users with Address Line 2": models.User.objects.exclude(
                address_line_2=""
            ).count(),
            "Users with Address City": models.User.objects.exclude(
                address_city=""
            ).count(),
            "Users with Address State": models.User.objects.exclude(
                address_state=""
            ).count(),
            "Users with Address Postcode": models.User.objects.exclude(
                address_postcode=""
            ).count(),
            "Users with Address Country": models.User.objects.exclude(
                address_country=""
            ).count(),
        }

        countries = models.User.objects.distinct("address_country").values_list(
            "address_country", flat=True
        )
        country_names = dict(django_countries.countries)
        for country in countries:
            try:
                country_name = country_names[country]
            except KeyError:
                country_name = f"Unkown Country ({ country })"

            user_stats[f"Users in { country_name }"] = models.User.objects.filter(
                address_country=country
            ).count()

        return {k: floor(n / users * 100) for k, n in user_stats.items()}

    def _get_exchange_percentages(self):  # pylint: disable=no-self-use
        """Exchange percentages."""

        percentages = {}

        users = models.User.objects.count()
        for exchange in models.Exchange.objects.upcoming():
            users_in_exchange = exchange.users.count()
            eligible_users_in_exchange = exchange.users.eligible_for_draw().count()
            percentages[f"Users in { exchange.name }"] = floor(
                users_in_exchange / users * 100
            )
            try:
                percentages[f"Eligible Users in { exchange.name }"] = floor(
                    eligible_users_in_exchange / users_in_exchange * 100
                )
                percentages[
                    f"Users ineligible due to unverified email in { exchange.name }"
                ] = floor(
                    exchange.users.filter(emailaddress__verified=False).count()
                    / users_in_exchange
                    * 100
                )
                percentages[
                    f"Users ineligible due to missing name in { exchange.name }"
                ] = floor(
                    exchange.users.filter(Q(first_name="") & Q(last_name="")).count()
                    / users_in_exchange
                    * 100
                )

            except ZeroDivisionError:
                pass

        return percentages

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["percentages"] = dict(
            **self._get_user_percentages(), **self._get_exchange_percentages()
        )
        context_data["users"] = models.User.objects.count()

        return context_data


class ManageFlatPages(LoginRequiredMixin, PermissionRequiredMixin, SingleTableView):
    """List flat pages."""

    permission_required = "af_gang_mail.view_flat_page"
    model = flatpages.models.FlatPage
    table_class = tables.FlatPage
    paginator_class = LazyPaginator


@method_decorator(csp_exempt, name="dispatch")
class CreateFlatPage(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Create flat page."""

    permission_required = "flatpage.add_flatpage"
    model = flatpages.models.FlatPage
    form_class = forms.FlatPage

    def get_success_url(self):
        return urls.reverse("manage-flatpages")


@method_decorator(csp_exempt, name="dispatch")
class UpdateFlatPage(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Modify flat page."""

    permission_required = "flatpage.change_flatpage"
    model = flatpages.models.FlatPage
    form_class = forms.FlatPage

    def get_success_url(self):
        return urls.reverse("manage-flatpages")


@csp_exempt
def edit_flatblock(request, pk, **kwargs):
    return flatblocks_views.edit(request, pk, modelform_class=forms.FlatBlock, **kwargs)


@login_required
def resend_verification(request):
    request.user.emailaddress_set.first().send_confirmation(request)
    messages.success(request, "A verification email is on its way!", fail_silently=True)
    return http.HttpResponseRedirect(urls.reverse("home"))
