from django.contrib import admin
from .models import Profile


def approve_user(modeladmin, request, queryset):
    for profile in queryset:
        profile.is_active = 'True'
        profile.save()


approve_user.short_description = 'Approve selected Profile'


def approve_superuser(modeladmin, request, queryset):
    for profile in queryset:
        profile.is_superuser = 'True'
        profile.save()


approve_superuser.short_description = 'Promote selected Profile to superuser'


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'contact', 'company', 'branch', 'department', 'is_active', 'is_superuser', 'is_staff')
    actions = [approve_user, approve_superuser]


admin.site.register(Profile, ProfileAdmin)
