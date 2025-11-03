from django.conf import settings
from django.db import models


class CategoryType(models.TextChoices):
    INCOME = 'income', 'Receita'
    EXPENSE = 'expense', 'Despesa'


CATEGORY_COLOR_CHOICES = [
    ('bg-indigo-500', 'Indigo'),
    ('bg-blue-500', 'Azul'),
    ('bg-purple-500', 'Roxo'),
    ('bg-green-500', 'Verde'),
    ('bg-emerald-500', 'Esmeralda'),
    ('bg-amber-500', 'Âmbar'),
    ('bg-pink-500', 'Rosa'),
    ('bg-red-500', 'Vermelho'),
]


class Category(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories',
    )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=CategoryType.choices, default=CategoryType.EXPENSE)
    color = models.CharField(max_length=30, choices=CATEGORY_COLOR_CHOICES, default='bg-indigo-500')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.name} ({self.get_type_display()})'
