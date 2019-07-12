from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'accounts'


urlpatterns = [
    path('login/', views.mylogin, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('signup', views.signup, name='signup'),
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html', success_url=reverse_lazy('accounts:password_reset_done')), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done')

]