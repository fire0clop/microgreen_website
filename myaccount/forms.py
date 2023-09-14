from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(UserCreationForm):
    company_name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'company_name', 'phone', 'password1', 'password2']
