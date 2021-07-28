from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser
from django.core.validators import RegexValidator

alphabet = RegexValidator(
    r'^[a-zA-Z]*$', 'Only alphabet characters are allowed.')


class LoginForm(forms.Form):
    email = forms.CharField(label="Email", widget=forms.EmailInput(
        attrs={'placeholder': 'email@domain.com'}), required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}), required=True)


class SignupForm(UserCreationForm):
    first_name = forms.CharField(
        label="First Name", required=True, validators=[alphabet])
    last_name = forms.CharField(
        label="Last Name", required=True, validators=[alphabet])
    email = forms.CharField(label="Email", widget=forms.EmailInput(
        attrs={'placeholder': 'email@domain.com'}), required=True)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
