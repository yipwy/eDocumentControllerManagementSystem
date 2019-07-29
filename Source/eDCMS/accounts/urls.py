from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'


urlpatterns = [
    path('login/', views.mylogin, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('signup', views.signup, name='signup'),
    path('reset-password/', views.MyPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.MyPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', views.profile, name='profile_page'),
    path('profile_update/', views.update_profile, name='profile_update'),
    path('password_change/', views.MyPasswordChangeView.as_view(), name='password_change'),
    path('ajax/load-department/', views.load_department, name='ajax_load_department'),
]