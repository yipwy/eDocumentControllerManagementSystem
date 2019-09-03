from django.contrib import admin
from .models import Profile


def approve_user(modeladmin, request, queryset):
    for profile in queryset:
        profile.is_active = 'True'
        profile.is_staff = 'True'
        profile.save()


approve_user.short_description = 'Activate selected Profile'


def disapprove_user(modeladmin, request, queryset):
    for profile in queryset:
        profile.is_active = 'False'
        profile.is_staff = 'False'
        profile.save()


disapprove_user.short_description = 'Deactivate selected Profile'


def approve_superuser(modeladmin, request, queryset):
    for profile in queryset:
        profile.is_superuser = 'True'
        profile.save()


approve_superuser.short_description = 'Promote selected Profile to superuser'


def deactivate_superuser(modeladmin, request, queryset):
    for profile in queryset:
        profile.is_superuser = 'False'
        profile.save()


deactivate_superuser.short_description = 'Demote selected Profile from superuser'


def approve_documentcontroller(modeladmin, request, queryset):
    for profile in queryset:
        profile.is_documentcontroller = 'True'
        profile.save()


approve_documentcontroller.short_description = 'Promote selected Profile to Doc-Controller'


def deactivate_documentcontroller(modeladmin, request, queryset):
    for profile in queryset:
        profile.is_documentcontroller = 'False'
        profile.save()


deactivate_documentcontroller.short_description = 'Demote selected Profile from Doc-Controller'


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'contact', 'email', 'company', 'branch', 'department',
                    'is_active', 'is_superuser', 'is_documentcontroller', 'is_staff')
    actions = [approve_user, disapprove_user, approve_superuser, deactivate_superuser, approve_documentcontroller,
               deactivate_documentcontroller]

    def save_model(self, request, obj, form, change):
        if obj.is_superuser is not True:
            obj.is_superuser = False
        if obj.is_documentcontroller is not True:
            obj.is_documentcontroller = False
        if obj.is_staff is not True:
            obj.is_staff = False
        if obj.is_active is not True:
            obj.is_active = False

        super().save_model(request, obj, form, change)


admin.site.register(Profile, ProfileAdmin)
