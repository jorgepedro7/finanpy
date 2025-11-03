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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_attrs = {
            'class': 'w-full bg-gray-900 border border-gray-700 rounded-md px-3 py-2 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500',
        }
        placeholders = {
            'email': 'nome@exemplo.com',
            'password1': 'mínimo de 8 caracteres',
            'password2': 'repita a senha',
        }
        for field_name, field in self.fields.items():
            attrs = base_attrs.copy()
            if field_name in placeholders:
                attrs['placeholder'] = placeholders[field_name]
            field.widget.attrs.update(attrs)
            field.help_text = ''


class UserChangeForm(DjangoUserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'is_active', 'is_staff', 'is_superuser')


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'autofocus': True}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_styles = {
            'class': 'w-full bg-gray-900 border border-gray-700 rounded-md px-3 py-2 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500',
        }
        self.fields['username'].widget.attrs.update(
            {**field_styles, 'placeholder': 'nome@exemplo.com', 'inputmode': 'email'}
        )
        self.fields['password'].widget.attrs.update(
            {**field_styles, 'placeholder': '••••••••'}
        )
