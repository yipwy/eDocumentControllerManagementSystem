from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


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

    return render(request, 'accounts/login.html')


def home(request):
    return render(request, 'accounts/home.html')
