from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from accounts.models import Account, AccountType


class AccountTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(email='user@example.com', password='testpass123')
        cls.other_user = get_user_model().objects.create_user(email='other@example.com', password='testpass123')
        cls.account = Account.objects.create(
            user=cls.user,
            name='Conta Principal',
            initial_balance=Decimal('100.00'),
            type=AccountType.CHECKING,
        )

    def test_str_representation(self):
        self.assertEqual(str(self.account), 'Conta Principal (Conta corrente)')

    def test_initial_balance_sets_current_balance(self):
        account = Account.objects.create(
            user=self.user,
            name='Reserva',
            initial_balance=Decimal('250.00'),
            type=AccountType.SAVINGS,
        )
        self.assertEqual(account.current_balance, Decimal('250.00'))

    def test_list_view_returns_only_user_accounts(self):
        Account.objects.create(
            user=self.other_user,
            name='Outra Conta',
            initial_balance=Decimal('50.00'),
            type=AccountType.CREDIT,
        )
        self.client.force_login(self.user)
        response = self.client.get(reverse('accounts:list'))

        self.assertEqual(response.status_code, 200)
        accounts = list(response.context['accounts'])
        self.assertTrue(all(account.user == self.user for account in accounts))
        self.assertEqual(response.context['total_balance'], self.account.current_balance)

    def test_create_view_assigns_user_and_sets_message(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('accounts:create'),
            data={
                'name': 'Nova Conta',
                'initial_balance': '350.00',
                'type': AccountType.CHECKING,
            },
            follow=True,
        )

        self.assertRedirects(response, reverse('accounts:list'))
        created_account = Account.objects.filter(user=self.user, name='Nova Conta').first()
        self.assertIsNotNone(created_account)
        self.assertEqual(created_account.current_balance, Decimal('350.00'))
        messages = [message.message for message in get_messages(response.wsgi_request)]
        self.assertIn('Conta criada com sucesso!', messages)

    def test_update_view_blocks_other_users_account(self):
        other_account = Account.objects.create(
            user=self.other_user,
            name='Conta Bloqueada',
            initial_balance=Decimal('75.00'),
            type=AccountType.SAVINGS,
        )
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('accounts:update', args=[other_account.pk]),
            data={
                'name': 'Conta Editada',
                'initial_balance': '80.00',
                'type': AccountType.SAVINGS,
            },
        )
        self.assertEqual(response.status_code, 404)
