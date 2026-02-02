from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
# UserAdmin needs adjustment for email-only auth but for now we register it simply
admin.site.register(CustomUser)
