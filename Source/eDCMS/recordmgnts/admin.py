from django.contrib import admin
from .models import Container
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.admin.models import LogEntry


class ContainerAdmin(SimpleHistoryAdmin):
    list_display = ('container_serial_number', 'container_description', 'status', 'created_by', 'department',
                    'created_date', 'modify_by', 'modify_date', 'warehouse', 'bay', 'row', 'column')
    history_list_display = ["status"]


admin.site.register(Container, ContainerAdmin)
admin.site.register(LogEntry)
admin.site.site_url = '/home'

