from decimal import Decimal

from django.conf import settings
from django.db import models

from accounts.models import Account
from categories.models import Category


class TransactionType(models.TextChoices):
    INCOME = 'income', 'Receita'
    EXPENSE = 'expense', 'Despesa'


class Transaction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions',
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='transactions',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions',
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    description = models.CharField(max_length=255, blank=True)
    transaction_date = models.DateField()
    type = models.CharField(max_length=20, choices=TransactionType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-transaction_date', '-created_at']
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return f'{self.get_type_display()} · {self.amount} · {self.transaction_date}'
