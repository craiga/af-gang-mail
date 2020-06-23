"""Views"""

from django.views.generic import TemplateView

from allauth.account.forms import LoginForm, SignupForm


class Home(TemplateView):
    """Home page."""

    extra_context = {
        "login_form": LoginForm(),
        "register_form": SignupForm(),
    }

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ["af_gang_mail/home/authenticated.html"]

        return ["af_gang_mail/home/unauthenticated.html"]
