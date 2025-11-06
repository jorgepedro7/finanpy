from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import Account, AccountType
from categories.models import CATEGORY_COLOR_CHOICES, Category, CategoryType
from transactions.models import Transaction, TransactionType


class CoreViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(email='dashboard@example.com', password='testpass123')
        cls.account = Account.objects.create(
            user=cls.user,
            name='Conta Corrente',
            initial_balance=Decimal('500.00'),
            type=AccountType.CHECKING,
        )
        cls.income_category = Category.objects.create(
            user=cls.user,
            name='Salário',
            type=CategoryType.INCOME,
            color=CATEGORY_COLOR_CHOICES[0][0],
        )
        cls.expense_category = Category.objects.create(
            user=cls.user,
            name='Alimentação',
            type=CategoryType.EXPENSE,
            color=CATEGORY_COLOR_CHOICES[1][0],
        )
        Transaction.objects.create(
            user=cls.user,
            account=cls.account,
            category=cls.income_category,
            amount=Decimal('1000.00'),
            transaction_date=date.today(),
            type=TransactionType.INCOME,
        )
        Transaction.objects.create(
            user=cls.user,
            account=cls.account,
            category=cls.expense_category,
            amount=Decimal('250.00'),
            transaction_date=date.today(),
            type=TransactionType.EXPENSE,
        )

    def test_home_view_is_accessible(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_authentication(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('users:login')))

    def test_dashboard_displays_financial_context(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_balance', response.context)
        self.assertIn('recent_transactions', response.context)
        self.assertEqual(response.context['category_counts']['income'], 1)
        self.assertEqual(response.context['category_counts']['expense'], 1)
        monthly_chart = response.context['dashboard_monthly_chart']
        self.assertEqual(len(monthly_chart['labels']), 6)
        self.assertAlmostEqual(monthly_chart['income'][-1], 1000.00)
        self.assertAlmostEqual(monthly_chart['expense'][-1], 250.00)
        self.assertAlmostEqual(monthly_chart['target'][-1], 800.00)

    def test_reports_view_aggregates_data(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('reports'), {'data_inicio': date.today().isoformat(), 'data_fim': date.today().isoformat()})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_income'], Decimal('1000.00'))
        self.assertEqual(response.context['total_expense'], Decimal('250.00'))
        self.assertIn('export_url', response.context)

    def test_reports_export_generates_csv(self):
        self.client.force_login(self.user)
        query = {'data_inicio': date.today().isoformat(), 'data_fim': date.today().isoformat()}
        response = self.client.get(reverse('reports_export'), query)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        today_stamp = date.today().strftime('%Y%m%d')
        disposition = response['Content-Disposition']
        self.assertIn(f'relatorio-financeiro-{today_stamp}-{today_stamp}.csv', disposition)
        payload = response.content.decode('utf-8')
        self.assertIn('Resumo;Período', payload)
        self.assertIn('Categoria;Salário;Receita;1000.00;0.00;1000.00', payload)
        self.assertIn('Categoria;Alimentação;Despesa;0.00;250.00;-250.00', payload)
        self.assertIn('Conta;Conta Corrente;Conta corrente;1000.00;250.00;750.00', payload)
