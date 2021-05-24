from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
# Create your views here.

from accounts.forms import CreateUser

class SignUp(CreateView):
    template_name = 'accounts/signup.html'
    form_class = CreateUser
    success_url = reverse_lazy('login')
