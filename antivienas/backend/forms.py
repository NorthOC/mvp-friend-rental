from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from antivienas.database.models import User, FriendSetting, Order, Dispute
from django import forms

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'city', 'gender', 'birthday', 'email', 'password']

class UserProfileUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['img_one', 'first_name', 'last_name', 'city', 'gender', 'birthday', 'personality_type', 'job', 'education', 'height_cm', 'interest_one', 'interest_two', 'interest_three', 'interest_four', 'interest_color_one', 'interest_color_two', 'interest_color_three', 'interest_color_four', 'description']

class FriendSettingsUpdateForm(ModelForm):
    class Meta:
        model = FriendSetting
        fields = ['price_per_hour', 'is_public']

class MeetingCreationForm(ModelForm):
    class Meta:
        model = Order
        fields  = ['meeting_day', 'meeting_hour', 'no_of_hours', 'meeting_place', 'comment', 'total_price', 'user', 'friend']

class MeetingCancelForm(ModelForm):
    class Meta:
        model = Order
        fields = ['cancel_reason', 'order_status']

class CreateDisputeForm(ModelForm):
    class Meta:
        model = Dispute
        fields = ['user_comment', 'friend_comment', 'order']