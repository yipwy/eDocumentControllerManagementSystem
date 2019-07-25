from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UserRegistrationForm, PasswordResetForm, ChangePasswordForm, CustomUserChangeForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


def mylogin(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            # correct username and password login the user
            login(request, user)
            return redirect('accounts:home')

        else:
            messages.warning(request, f'Incorrect username or password.')

    return render(request, 'registration/login.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created.')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/signup.html', {'form': form})


class MyPasswordResetView(auth_views.PasswordResetView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:home')
        return super(MyPasswordResetView, self).get(request, *args, **kwargs)


class MyPasswordConfirmView(auth_views.PasswordResetConfirmView):
    form_class = PasswordResetForm


class MyPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:home')
        return super(MyPasswordResetCompleteView, self).get(request, *args, **kwargs)


class MyPasswordChangeView(SuccessMessageMixin, auth_views.PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('accounts:profile_page')

    def get_success_message(self, cleaned_data):
        return 'Your password has been changed successfully.'


@login_required
def home(request):
    return render(request, 'accounts/home.html')


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your profile has been updated.')
            return redirect('accounts:profile_page')

    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/profile_update_form.html', {'form': form})