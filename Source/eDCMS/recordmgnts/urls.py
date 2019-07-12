from django.urls import path
from . import views

app_name = 'recordmgnts'


urlpatterns = [
    path('records/', views.showTable, name='records'),
]