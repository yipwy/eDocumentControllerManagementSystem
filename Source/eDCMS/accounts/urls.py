from django.urls import path
from . import views


app_name = 'accounts'


urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('index/', views.index, name='index')
]