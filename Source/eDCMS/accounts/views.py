from django.shortcuts import render, redirect

from django.contrib.auth.views import LoginView


class MyLoginView(LoginView):
    template_name = 'accounts/login.html'







def index(request):
    return render(request, 'accounts/index.html')
