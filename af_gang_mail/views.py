"""Views"""

from django.views.generic import TemplateView

from allauth.account.forms import LoginForm, SignupForm


class Home(TemplateView):
    template_name = "af_gang_mail/home.html"
    extra_context = {
        "login_form": LoginForm(),
        "register_form": SignupForm(),
    }
