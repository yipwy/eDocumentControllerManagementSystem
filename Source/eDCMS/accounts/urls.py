from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'


urlpatterns = [
    path('login/', views.mylogin, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('signup', views.signup, name='signup')

]