from django.contrib import admin
from .models import Profile


def approve_user(modeladmin, request, queryset):
    for profile in queryset:
        profile.is_active = 'True'
        profile.is_staff = 'True'
        profile.save()


approve_user.short_description = 'Approve selected Profile'


def disapprove_user(modeladmin, request, queryset):
    for profile in queryset:
        profile.is_active = 'False'
        profile.save()


disapprove_user.short_description = 'Disapprove selected Profile'


def approve_superuser(modeladmin, request, queryset):
    for profile in queryset:
        profile.is_superuser = 'True'
        profile.save()


approve_superuser.short_description = 'Promote selected Profile to superuser'


def deactivate_superuser(modeladmin, request, queryset):
    for profile in queryset:
        profile.is_superuser = 'False'
        profile.save()


deactivate_superuser.short_description = 'Deactivate selected Profile from superuser'


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'contact', 'email', 'company', 'branch', 'department', 'is_active', 'is_superuser', 'is_staff')
    actions = [approve_user, disapprove_user, approve_superuser, deactivate_superuser]


admin.site.register(Profile, ProfileAdmin)
