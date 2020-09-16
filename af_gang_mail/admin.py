"""Admin"""

from django.contrib import admin, auth

from af_gang_mail import models


@admin.register(models.User)
class UserAdmin(auth.admin.UserAdmin):
    change_form_template = "admin/auth/user/change_form.html"
    change_list_template = "admin/auth/user/change_list.html"
    list_filter = ["address_country"]
    fieldsets = auth.admin.UserAdmin.fieldsets + (
        (
            "Address",
            {
                "fields": [
                    "address_line_1",
                    "address_line_2",
                    "address_city",
                    "address_state",
                    "address_postcode",
                    "address_country",
                ]
            },
        ),
    )


@admin.register(models.Draw)
class DrawAdmin(admin.ModelAdmin):
    list_display = ["sender", "recipient", "exchange"]
    list_filter = ["exchange"]


@admin.register(models.Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ["name", "drawn", "sent"]
