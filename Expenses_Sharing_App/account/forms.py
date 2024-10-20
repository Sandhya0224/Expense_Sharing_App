from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

class CustomCreationForm(UserCreationForm):
    phone = forms.CharField(max_length=15, required=False)
    class Meta:
        model = get_user_model()
        fields = ['username', 'email','phone', 'password1', 'password2']