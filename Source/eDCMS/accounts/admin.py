from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'contact', 'branch', 'department', 'is_superuser', 'is_staff')


admin.site.register(Profile, ProfileAdmin)
