from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm as DjangoUserChangeForm,
    UserCreationForm as DjangoUserCreationForm,
)

from .models import User


class UserCreationForm(DjangoUserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class UserChangeForm(DjangoUserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'is_active', 'is_staff', 'is_superuser')


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'autofocus': True}))
