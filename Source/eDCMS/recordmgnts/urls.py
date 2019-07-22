from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'recordmgnts'


urlpatterns = [
    path('records/', views.showContainer, name='records'),
    path('records/new_container', views.addContainer, name='new_container'),
    path('records/new_container/SuccessAdded', TemplateView.as_view(template_name="SuccessAdded.html"), name='success')
]