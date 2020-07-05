"""Forms"""

from django import forms
from django.utils.timezone import now

from allauth.account import forms as allauth_forms
from ckeditor.widgets import CKEditorWidget
from flatblocks import forms as flatblock_forms

from af_gang_mail import models


class UpdateNameAndAddress(forms.ModelForm):
    """Update name and address."""

    address_search = forms.CharField(required=False)

    class Meta:
        model = models.User
        widgets = {
            "address_search": forms.TextInput(),
            "address_line_1": forms.TextInput(),
            "address_line_2": forms.TextInput(),
            "address_city": forms.TextInput(),
            "address_state": forms.TextInput(),
            "address_postcode": forms.TextInput(),
        }
        fields = [
            "first_name",
            "last_name",
            "address_search",
            "address_line_1",
            "address_line_2",
            "address_city",
            "address_state",
            "address_postcode",
            "address_country",
        ]


class SelectExchanges(forms.ModelForm):
    """Update selected exchanges."""

    exchanges = forms.ModelMultipleChoiceField(
        queryset=models.Exchange.objects.filter(drawn__gt=now()).order_by("drawn"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = models.User
        fields = [
            "exchanges",
        ]


class Exchange(forms.ModelForm):
    """Manage exchange form."""

    class Meta:
        model = models.Exchange
        widgets = {
            "name": forms.TextInput(),
        }
        fields = ["name", "drawn", "sent", "received"]


def _fix_email(value):
    return value.replace("e-mail", "email").replace("E-mail", "Email")


class AllauthFormWithEmailMixin:
    """Mixin to replace 'e-mail' with 'email' in fields."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = _fix_email(field.label)
            if "placeholder" in field.widget.attrs:
                field.widget.attrs["placeholder"] = _fix_email(
                    field.widget.attrs["placeholder"]
                )


class LoginForm(AllauthFormWithEmailMixin, allauth_forms.LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["login"].widget.attrs.pop("autofocus", None)


class ResetPasswordForm(AllauthFormWithEmailMixin, allauth_forms.ResetPasswordForm):
    pass


class SignupForm(AllauthFormWithEmailMixin, allauth_forms.SignupForm):
    pass


class FlatBlock(flatblock_forms.FlatBlockForm):
    class Meta(flatblock_forms.FlatBlockForm.Meta):
        widgets = {"content": CKEditorWidget()}
