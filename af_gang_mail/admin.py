"""Admin"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from af_gang_mail import models

admin.site.register(models.User, UserAdmin)


@admin.register(models.Draw)
class DrawAdmin(admin.ModelAdmin):
    list_display = ["sender", "recipient", "exchange"]
    list_filter = ["exchange"]


@admin.register(models.Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ["name", "drawn", "sent"]
