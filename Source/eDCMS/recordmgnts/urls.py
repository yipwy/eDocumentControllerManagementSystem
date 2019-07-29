from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'recordmgnts'


urlpatterns = [
    path('records/', views.showContainer, name='records'),
    path('records/new_container', views.addContainer, name='new_container'),
    path('records/new_container/success_added', TemplateView.as_view(template_name="success_added.html"), name='success'),
    path('<int:id>/', views.ContainerDetailView.as_view(), name='container_view'),
    path('delete/<int:id>/', views.containerDelete, name='container_delete'),
    path('search/', views.SearchContainerView.as_view(), name='container_search'),
    path('records/edit_records/<int:pk>/', views.containerUpdate, name='edit_records'),
    path('transaction/', views.transaction_log, name='transaction_log'),
    path('load_document_series/', views.load_series_number, name='ajax_load_doc_number'),
    path('ajax/load-locations/', views.load_locations, name='ajax_load_locations'),
    path('ajax/load-containers/', views.load_containers, name='ajax_load_containers'),
]