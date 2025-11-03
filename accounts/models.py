from decimal import Decimal

from django.conf import settings
from django.db import models


class AccountType(models.TextChoices):
    CHECKING = 'checking', 'Conta corrente'
    SAVINGS = 'savings', 'Poupança'
    CREDIT = 'credit', 'Cartão de crédito'


class Account(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts',
    )
    name = models.CharField(max_length=100)
    initial_balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    current_balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    type = models.CharField(max_length=20, choices=AccountType.choices, default=AccountType.CHECKING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return f'{self.name} ({self.get_type_display()})'

    def save(self, *args, **kwargs):
        if self._state.adding and self.current_balance == Decimal('0.00'):
            self.current_balance = self.initial_balance
        super().save(*args, **kwargs)
