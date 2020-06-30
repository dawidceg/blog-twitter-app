from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.shortcuts import redirect, render
from . import forms

# Create your views here.
class SignUp(CreateView):
    form_class = forms.UserCreateForm           # uses form UserCreateForm
    success_url = reverse_lazy("login")         # if the form is OK, go to the login page
    template_name = "accounts/signup.html"      
