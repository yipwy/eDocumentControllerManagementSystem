from django.contrib import admin

# Register your models here.
from .models import Container

admin.site.register(Container)
admin.site.site_url = '/home'