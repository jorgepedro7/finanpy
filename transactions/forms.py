from decimal import Decimal

from django import forms

from accounts.models import Account
from categories.models import Category, CategoryType

from .models import Transaction, TransactionType


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('transaction_date', 'type', 'account', 'category', 'amount', 'description')
        labels = {
            'transaction_date': 'Data',
            'type': 'Tipo',
            'account': 'Conta',
            'category': 'Categoria',
            'amount': 'Valor',
            'description': 'Descrição',
        }
        widgets = {
            'transaction_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full bg-gray-800 border border-gray-700 rounded-md px-3 py-2 text-white'}),
            'type': forms.Select(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded-md px-3 py-2 text-white'}),
            'account': forms.Select(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded-md px-3 py-2 text-white'}),
            'category': forms.Select(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded-md px-3 py-2 text-white'}),
            'amount': forms.NumberInput(
                attrs={
                    'class': 'w-full bg-gray-800 border border-gray-700 rounded-md px-3 py-2 text-white',
                    'min': '0',
                    'step': '0.01',
                }
            ),
            'description': forms.TextInput(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded-md px-3 py-2 text-white'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['account'].queryset = Account.objects.filter(user=self.user).order_by('name')
            self.fields['category'].queryset = Category.objects.filter(user=self.user).order_by('name')
        self.fields['category'].required = False

    def clean_amount(self):
        amount = self.cleaned_data.get('amount') or Decimal('0.00')
        if amount <= 0:
            raise forms.ValidationError('Informe um valor positivo para a transação.')
        return amount

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        transaction_type = cleaned_data.get('type')
        if category and transaction_type:
            if transaction_type == TransactionType.INCOME and category.type != CategoryType.INCOME:
                self.add_error('category', 'Selecione uma categoria do tipo receita.')
            if transaction_type == TransactionType.EXPENSE and category.type != CategoryType.EXPENSE:
                self.add_error('category', 'Selecione uma categoria do tipo despesa.')
        return cleaned_data
