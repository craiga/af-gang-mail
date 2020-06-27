"""Forms"""

from django import forms
from django.utils.timezone import now

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
    )

    class Meta:
        model = models.User
        fields = [
            "exchanges",
        ]
