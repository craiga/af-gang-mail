"""URLs."""

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import permission_required
from django.contrib.flatpages.views import flatpage
from django.urls import include, path, re_path

from af_gang_mail import views

urlpatterns = [
    path("in-case-of-emergency/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("su/", include("django_su.urls")),
    path(
        "__edit__/<pk>/",
        permission_required("flatblocks.change_flatblock")(views.edit_flatblock),
        name="edit-flatblock",
    ),
    path(
        "update-name-and-address/",
        views.UpdateNameAndAddress.as_view(),
        name="update-name-and-address",
    ),
    path("select-exchanges/", views.SelectExchanges.as_view(), name="select-exchanges"),
    path("create-exchange/", views.CreateExchange.as_view(), name="create-exchange"),
    path(
        "manage-exchanges/<slug:slug>/edit/",
        views.UpdateExchange.as_view(),
        name="update-exchange",
    ),
    path(
        "manage-exchanges/<slug:slug>/delete/",
        views.DeleteExchange.as_view(),
        name="delete-exchange",
    ),
    path(
        "manage-exchanges/<slug:slug>/draw/",
        views.DrawExchange.as_view(),
        name="draw-exchange",
    ),
    path(
        "manage-exchanges/<slug:slug>/delete-draws/",
        views.DeleteDrawsForExchange.as_view(),
        name="delete-draws-for-exchange",
    ),
    path(
        "manage-exchanges/draws/<int:pk>/", views.ViewDraw.as_view(), name="view-draw"
    ),
    path(
        "manage-exchanges/<slug:slug>/",
        views.ViewExchange.as_view(),
        name="view-exchange",
    ),
    path("manage-exchanges/", views.ManageExchanges.as_view(), name="manage-exchanges"),
    path("create-flatpage/", views.CreateFlatPage.as_view(), name="create-flatpage"),
    path(
        "manage-flatpages/<int:pk>/edit/",
        views.UpdateFlatPage.as_view(),
        name="update-flatpage",
    ),
    path("manage-flatpages/", views.ManageFlatPages.as_view(), name="manage-flatpages"),
    path("style-gallery/", views.StyleGallery.as_view(), name="style-gallery"),
    path("page-index/", views.PageIndex.as_view(), name="page-index"),
    path("home/", views.Home.as_view(), name="home"),
    path(
        "welcome/name-and-address/",
        views.SignUpStepOne.as_view(),
        name="sign-up-step-one",
    ),
    path("welcome/exchanges/", views.SignUpStepTwo.as_view(), name="sign-up-step-two"),
    path("resend-verification/", views.resend_verification, name="resend-verification"),
    path("tz_detect/", include("tz_detect.urls")),
    path("exchange/<slug:slug>/sent/", views.MailSent.as_view(), name="draw-sent"),
    path(
        "exchange/<slug:slug>/received/",
        views.MailReceived.as_view(),
        name="draw-received",
    ),
    path("exchange/<slug:slug>/", views.Draw.as_view(), name="draw"),
    path("statto/", views.Statto.as_view(), name="statto"),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    re_path(r"^(?P<url>.*/)$", flatpage),
    path("", views.Landing.as_view(), name="landing"),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
