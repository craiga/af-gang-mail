"""Forms"""

from django import forms, template
from django.contrib import flatpages
from django.utils.timezone import now

from allauth.account import forms as allauth_forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
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
            "address_country",
            "address_search",
            "address_line_1",
            "address_line_2",
            "address_city",
            "address_state",
            "address_postcode",
        ]


class SelectExchangeField(forms.ModelMultipleChoiceField):
    """Select exchange field."""

    def get_limit_choices_to(self):
        return models.Exchange.objects.get_upcoming_filter_kwargs()

    def label_from_instance(self, obj):
        label_template = template.loader.get_template(
            "af_gang_mail/_exchange-label.html"
        )
        return label_template.render({"exchange": obj})


class SelectExchanges(forms.ModelForm):
    """Update selected exchanges."""

    exchanges = SelectExchangeField(
        queryset=models.Exchange.objects.order_by("drawn"),
        widget=forms.CheckboxSelectMultiple,
        label="",
        required=False,
    )

    class Meta:
        model = models.User
        fields = ["exchanges"]

    def clean(self):
        super().clean()

        # Re-add exchanges which aren't included in this form's UI.
        self.cleaned_data["exchanges"] |= self.instance.exchanges.not_upcoming()

        return self.cleaned_data

    def save(self, commit=True):
        """If joining an exchange after the confirmation reminder, confirm it."""

        previous_exchanges = set(self.instance.exchanges.all())
        result = super().save(commit)
        if commit:
            for exchange in self.instance.exchanges.all():
                if exchange not in previous_exchanges:
                    if (
                        exchange.confirmation_reminder
                        and exchange.confirmation_reminder < now()
                    ):
                        models.UserInExchange.objects.filter(
                            user=self.instance, exchange=exchange
                        ).update(confirmed=True)

        return result


class Exchange(forms.ModelForm):
    """Manage exchange form."""

    class Meta:
        model = models.Exchange
        widgets = {
            "name": forms.TextInput(),
        }
        fields = [
            "name",
            "confirmation",
            "confirmation_reminder",
            "drawn",
            "sent",
            "received",
            "send_emails",
        ]


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
    """Sign up form."""

    agree = forms.BooleanField(
        label="Yes, this site can store my data",
        required=True,
        help_text=(
            "In order to participate in the mail exchange, we require your email "
            "address, name, and postal address. <a href='/privacy'>Our privacy "
            "document explains how we store and use this information</a>. Without "
            "those details, we're not able to run the mail exchange. Sorry!"
        ),
    )

    field_order = ["email", "password1", "agree"]


class FlatBlock(flatblock_forms.FlatBlockForm):
    class Meta(flatblock_forms.FlatBlockForm.Meta):
        widgets = {"content": CKEditorUploadingWidget()}


class FlatPage(flatpages.forms.FlatpageForm):
    class Meta(flatpages.forms.FlatpageForm.Meta):
        widgets = {"content": CKEditorUploadingWidget()}


class MailSent(forms.Form):
    message = forms.CharField(widget=forms.Textarea(), required=False)


class MailReceived(forms.Form):
    message = forms.CharField(widget=forms.Textarea(), required=False)
