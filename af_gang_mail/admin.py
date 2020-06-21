"""Admin"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from af_gang_mail import models

admin.site.register(models.User, UserAdmin)
