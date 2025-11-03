from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from accounts.models import Account, AccountType
from categories.models import CATEGORY_COLOR_CHOICES, Category, CategoryType
from transactions.forms import TransactionForm
from transactions.models import Transaction, TransactionType


class TransactionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(email='user@example.com', password='testpass123')
        cls.account = Account.objects.create(
            user=cls.user,
            name='Conta Corrente',
            initial_balance=Decimal('100.00'),
            type=AccountType.CHECKING,
        )
        cls.secondary_account = Account.objects.create(
            user=cls.user,
            name='Poupança',
            initial_balance=Decimal('200.00'),
            type=AccountType.SAVINGS,
        )
        cls.income_category = Category.objects.create(
            user=cls.user,
            name='Salário',
            type=CategoryType.INCOME,
            color=CATEGORY_COLOR_CHOICES[0][0],
        )
        cls.expense_category = Category.objects.create(
            user=cls.user,
            name='Aluguel',
            type=CategoryType.EXPENSE,
            color=CATEGORY_COLOR_CHOICES[1][0],
        )

    def _create_transaction(self, **overrides):
        defaults = {
            'user': self.user,
            'account': self.account,
            'category': self.income_category,
            'amount': Decimal('50.00'),
            'transaction_date': date(2024, 1, 1),
            'type': TransactionType.INCOME,
        }
        defaults.update(overrides)
        return Transaction.objects.create(**defaults)

    def test_form_rejects_non_positive_amount(self):
        form = TransactionForm(
            data={
                'transaction_date': '2024-01-01',
                'type': TransactionType.INCOME,
                'account': self.account.pk,
                'category': self.income_category.pk,
                'amount': '0',
                'description': '',
            },
            user=self.user,
        )
        self.assertFalse(form.is_valid())
        self.assertIn('Informe um valor positivo para a transação.', form.errors['amount'])

    def test_form_validates_category_matches_type(self):
        form = TransactionForm(
            data={
                'transaction_date': '2024-01-01',
                'type': TransactionType.INCOME,
                'account': self.account.pk,
                'category': self.expense_category.pk,
                'amount': '100.00',
                'description': '',
            },
            user=self.user,
        )
        self.assertFalse(form.is_valid())
        self.assertIn('Selecione uma categoria do tipo receita.', form.errors['category'])

    def test_create_view_updates_account_balance(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('transactions:create'),
            data={
                'transaction_date': '2024-02-01',
                'type': TransactionType.INCOME,
                'account': self.account.pk,
                'category': self.income_category.pk,
                'amount': '150.00',
                'description': 'Bônus',
            },
            follow=True,
        )
        self.assertRedirects(response, reverse('transactions:list'))
        self.account.refresh_from_db()
        self.assertEqual(self.account.current_balance, Decimal('250.00'))
        messages = [message.message for message in get_messages(response.wsgi_request)]
        self.assertIn('Transação registrada com sucesso!', messages)

    def test_update_view_recalculates_previous_and_new_account(self):
        transaction = self._create_transaction()
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('transactions:update', args=[transaction.pk]),
            data={
                'transaction_date': '2024-01-15',
                'type': TransactionType.EXPENSE,
                'account': self.secondary_account.pk,
                'category': self.expense_category.pk,
                'amount': '30.00',
                'description': 'Transferência',
            },
            follow=True,
        )
        self.assertRedirects(response, reverse('transactions:list'))
        self.account.refresh_from_db()
        self.secondary_account.refresh_from_db()
        self.assertEqual(self.account.current_balance, Decimal('100.00'))
        self.assertEqual(self.secondary_account.current_balance, Decimal('170.00'))

    def test_delete_view_reverts_account_balance(self):
        transaction = self._create_transaction(amount=Decimal('40.00'))
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('transactions:delete', args=[transaction.pk]),
            follow=True,
        )
        self.assertRedirects(response, reverse('transactions:list'))
        self.account.refresh_from_db()
        self.assertEqual(self.account.current_balance, Decimal('100.00'))

    def test_list_view_filters_by_month_and_year(self):
        self._create_transaction(transaction_date=date(2024, 1, 10), amount=Decimal('60.00'))
        self._create_transaction(transaction_date=date(2024, 2, 5), amount=Decimal('70.00'))
        self.client.force_login(self.user)
        response = self.client.get(reverse('transactions:list'), {'month': '1', 'year': '2024'})
        self.assertEqual(response.status_code, 200)
        transactions = list(response.context['transactions'])
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].transaction_date.month, 1)
