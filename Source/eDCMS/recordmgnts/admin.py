from django.contrib import admin
from .models import Container, ContainerInstance
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.admin.models import LogEntry


def delete_container(modeladmin, request, queryset):
    for obj in queryset:
        obj.is_deleted = True
        if obj.status is not True:
            obj.status = False
        obj.save()
        
delete_container.short_description = 'Delete selected containers'


def recover_container(modeladmin, request, queryset):
    for obj in queryset:
        obj.is_deleted = False
        if obj.status is not True:
            obj.status = False
        obj.save()
        
recover_container.short_description = 'Recover selected containers'


class ContainerAdmin(SimpleHistoryAdmin):
    list_display = ('container_serial_number', 'container_description', 'status', 'created_by', 'department',
                    'created_date', 'modify_by', 'modify_date', 'warehouse', 'bay', 'row', 'column', 'is_deleted')
    history_list_display = ["status"]
    actions = [delete_container, recover_container]
    
    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if obj.is_deleted is not True:
            obj.is_deleted = False

        super().save_model(request, obj, form, change)


class ContainerInstanceAdmin(admin.ModelAdmin):
    list_display = ('container', 'due_date', 'is_returned', 'user')
    actions      = None
    
    def has_add_permission(self, request):
        return False
        
    def __init__(self, *args, **kwargs):
        super(ContainerInstanceAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = None


admin.site.register(Container, ContainerAdmin)
admin.site.register(ContainerInstance, ContainerInstanceAdmin)
admin.site.register(LogEntry)
admin.site.site_url = '/'
admin.site.site_header = 'eDCMS Administration'

