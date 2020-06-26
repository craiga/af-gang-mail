"""URLs."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from af_gang_mail import views

urlpatterns = [
    path("in-case-of-emergency/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path(
        "update-name-and-address/",
        views.UpdateNameAndAddress.as_view(),
        name="update-name-and-address",
    ),
    path(
        "select-exchanges/", views.SelectExchanges.as_view(), name="select-exchanges",
    ),
    path(
        "manage-exchanges/", views.ManageExchanges.as_view(), name="manage-exchanges",
    ),
    path("", views.Home.as_view(), name="home"),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls)),] + urlpatterns
