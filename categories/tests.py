from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from categories.models import CATEGORY_COLOR_CHOICES, Category, CategoryType


class CategoryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(email='user@example.com', password='testpass123')
        cls.other_user = get_user_model().objects.create_user(email='guest@example.com', password='testpass123')
        cls.category_income = Category.objects.create(
            user=cls.user,
            name='Salário',
            type=CategoryType.INCOME,
            color=CATEGORY_COLOR_CHOICES[0][0],
        )
        cls.category_expense = Category.objects.create(
            user=cls.user,
            name='Aluguel',
            type=CategoryType.EXPENSE,
            color=CATEGORY_COLOR_CHOICES[1][0],
        )

    def test_str_representation(self):
        self.assertEqual(str(self.category_income), 'Salário (Receita)')

    def test_list_view_counts_types(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('categories:list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['income_count'], 1)
        self.assertEqual(response.context['expense_count'], 1)
        categories = list(response.context['categories'])
        self.assertEqual(len(categories), 2)

    def test_create_view_assigns_user_and_message(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('categories:create'),
            data={
                'name': 'Lazer',
                'type': CategoryType.EXPENSE,
                'color': CATEGORY_COLOR_CHOICES[2][0],
            },
            follow=True,
        )
        self.assertRedirects(response, reverse('categories:list'))
        category = Category.objects.filter(user=self.user, name='Lazer').first()
        self.assertIsNotNone(category)
        messages = [message.message for message in get_messages(response.wsgi_request)]
        self.assertIn('Categoria criada com sucesso!', messages)

    def test_update_view_returns_404_for_other_user_category(self):
        foreign_category = Category.objects.create(
            user=self.other_user,
            name='Combustível',
            type=CategoryType.EXPENSE,
            color=CATEGORY_COLOR_CHOICES[3][0],
        )
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('categories:update', args=[foreign_category.pk]),
            data={
                'name': 'Gasolina',
                'type': CategoryType.EXPENSE,
                'color': CATEGORY_COLOR_CHOICES[3][0],
            },
        )
        self.assertEqual(response.status_code, 404)
