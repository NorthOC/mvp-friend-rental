from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from antivienas.database.models import User
from django import forms

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'city', 'gender', 'birthday', 'email', 'password']

class UserProfileUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'city', 'gender', 'birthday', 'personality_type', 'job', 'education', 'height_cm', 'interest_one', 'interest_two', 'interest_three', 'interest_four', 'interest_color_one', 'interest_color_two', 'interest_color_three', 'interest_color_four']

class UserDescriptionUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['description']