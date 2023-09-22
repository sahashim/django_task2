from django import forms
from users.models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.ModelForm):
    email = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']