from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from antivienas.database.models import User
from django import forms

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'city', 'gender', 'birthday', 'email', 'password']