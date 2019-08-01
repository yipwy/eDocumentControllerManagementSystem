from django.contrib import admin
from .models import Container
from simple_history.admin import SimpleHistoryAdmin


class ContainerAdmin(SimpleHistoryAdmin):
    list_display = ('container_serial_number', 'container_description', 'status', 'created_by', 'created_date',
                    'modify_by', 'modify_date', 'warehouse', 'location')
    history_list_display = ["status"]


admin.site.register(Container, ContainerAdmin)
admin.site.site_url = '/home'

