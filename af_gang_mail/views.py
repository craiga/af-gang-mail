"""Views"""

from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = "af_gang_mail/home.html"
