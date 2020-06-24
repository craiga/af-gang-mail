"""Views"""

from django import urls
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, UpdateView

from allauth.account.forms import LoginForm, SignupForm

from af_gang_mail import forms


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
