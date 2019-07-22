from django.urls import path
from . import views

app_name = 'recordmgnts'


urlpatterns = [
    path('records/', views.showContainer, name='records'),
    path('<int:id>/', views.ContainerDetailView.as_view(), name='records_view'),
    path('delete/<int:id>/', views.containerDelete, name='records_delete'),
]