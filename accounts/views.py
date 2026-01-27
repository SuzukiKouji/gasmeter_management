from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

class LoginView(LoginView):
    form_class = AuthenticationForm  # ← ここに適切な認証フォームを指定
    template_name = 'accounts/login.html'