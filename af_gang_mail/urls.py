"""URLs."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.decorators import login_required

from flatblocks import views as flatblocks_views

from af_gang_mail import views

urlpatterns = [
    path("in-case-of-emergency/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("flatblocks/<pk>/edit/", login_required(flatblocks_views.edit), name='flatblocks-edit'),
    path(
        "update-name-and-address/",
        views.UpdateNameAndAddress.as_view(),
        name="update-name-and-address",
    ),
    path(
        "select-exchanges/", views.SelectExchanges.as_view(), name="select-exchanges",
    ),
    path(
        "manage-exchanges/<slug:slug>/delete",
        views.DeleteExchange.as_view(),
        name="delete-exchange",
    ),
    path(
        "manage-exchanges/<slug:slug>/draw",
        views.DrawExchange.as_view(),
        name="draw-exchange",
    ),
    path(
        "manage-exchanges/<slug:slug>",
        views.ViewExchange.as_view(),
        name="view-exchange",
    ),
    path(
        "manage-exchanges/", views.ManageExchanges.as_view(), name="manage-exchanges",
    ),
    path("style-gallery/", views.StyleGallery.as_view(), name="style-gallery",),
    path("home/", views.Home.as_view(), name="home"),
    path(
        "welcome/name-and-address",
        views.SignUpStepOne.as_view(),
        name="sign-up-step-one",
    ),
    path("welcome/exchanges", views.SignUpStepTwo.as_view(), name="sign-up-step-two"),
    path("", views.Landing.as_view(), name="landing"),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls)),] + urlpatterns
