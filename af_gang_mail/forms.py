"""Forms"""

from django import forms, template

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


class SelectExchangeField(forms.ModelMultipleChoiceField):
    """Select exchange field."""

    def label_from_instance(self, obj):
        label_template = template.loader.get_template(
            "af_gang_mail/_exchange-label.html"
        )
        return label_template.render({"exchange": obj})


class SelectExchanges(forms.ModelForm):
    """Update selected exchanges."""

    exchanges = SelectExchangeField(
        queryset=models.Exchange.objects.upcoming().order_by("drawn"),
        widget=forms.CheckboxSelectMultiple,
        label="",
        required=False,
    )

    class Meta:
        model = models.User
        fields = [
            "exchanges",
        ]

    def clean(self):
        super().clean()

        # Re-add exchanges which aren't included in this form's UI.
        self.cleaned_data["exchanges"] |= self.instance.exchanges.not_upcoming()

        return self.cleaned_data


class Exchange(forms.ModelForm):
    """Manage exchange form."""

    class Meta:
        model = models.Exchange
        widgets = {
            "name": forms.TextInput(),
        }
        fields = ["name", "drawn", "sent", "received", "send_emails"]


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
    agree = forms.BooleanField(
        label="Yes, this site can store my data",
        required=True,
        help_text=(
            "In order to participate in the mail exchange, we require your email address, name, "
            "and postal address. <a href='/privacy'>Our privacy document explains how we  store "
            "and use this information</a>. Without those details, we're not able to run the mail "
            "exchange. Sorry!"
        ),
    )

    field_order = ["email", "password1", "agree"]


class FlatBlock(flatblock_forms.FlatBlockForm):
    class Meta(flatblock_forms.FlatBlockForm.Meta):
        widgets = {"content": CKEditorWidget()}
