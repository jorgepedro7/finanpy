from decimal import Decimal

from django import forms

from .models import Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('name', 'initial_balance', 'type')
        labels = {
            'name': 'Nome da conta',
            'initial_balance': 'Saldo inicial',
            'type': 'Tipo',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded-md px-3 py-2 text-white'}),
            'initial_balance': forms.NumberInput(
                attrs={
                    'class': 'w-full bg-gray-800 border border-gray-700 rounded-md px-3 py-2 text-white',
                    'min': '0',
                    'step': '0.01',
                }
            ),
            'type': forms.Select(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded-md px-3 py-2 text-white'}),
        }

    def clean_initial_balance(self):
        initial_balance = self.cleaned_data.get('initial_balance') or Decimal('0.00')
        if initial_balance < 0:
            raise forms.ValidationError('O saldo inicial deve ser maior ou igual a zero.')
        return initial_balance
