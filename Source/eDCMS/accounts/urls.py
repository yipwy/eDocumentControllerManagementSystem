from django.urls import path
from . import views


app_name = 'accounts'


urlpatterns = [
    path('login/', views.mylogin, name='login'),
    path('index/', views.index, name='index')
]