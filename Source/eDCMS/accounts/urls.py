from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from .forms import UserCreationForm

app_name = 'accounts'


urlpatterns = [
    path('login/', views.mylogin, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('signup', views.signup, name='signup'),
    path('reset-password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.MyPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]