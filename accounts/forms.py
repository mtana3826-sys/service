from django import forms
from django.contrib.auth.forms import AuthenticationForm

class PhoneLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Телефон",
        widget=forms.TextInput(attrs={"placeholder": "Номер телефона"})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput()
    )