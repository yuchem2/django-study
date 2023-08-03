
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email"]


class PasswordFindForm(forms.Form):
    username = forms.CharField(max_length=20, label="사용자이름")
    email = forms.EmailField(label="이메일")


class PasswordForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["password1", "password2"]


class IDFindForm(forms.Form):
    email = forms.EmailField(label="이메일")
