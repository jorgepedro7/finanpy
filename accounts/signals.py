from decimal import Decimal

from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from accounts.models import Account
from transactions.models import Transaction, TransactionType


def recalculate_account_balance(account_id):
    account = Account.objects.filter(id=account_id).first()
    if not account:
        return
    totals = account.transactions.aggregate(
        income=Coalesce(Sum('amount', filter=Q(type=TransactionType.INCOME)), Decimal('0.00')),
        expense=Coalesce(Sum('amount', filter=Q(type=TransactionType.EXPENSE)), Decimal('0.00')),
    )
    account.current_balance = account.initial_balance + totals['income'] - totals['expense']
    account.save(update_fields=['current_balance'])


@receiver(pre_save, sender=Transaction)
def track_previous_account(sender, instance, **kwargs):
    if not instance.pk:
        instance._previous_account_id = None
        return
    try:
        previous = Transaction.objects.get(pk=instance.pk)
        instance._previous_account_id = previous.account_id
    except Transaction.DoesNotExist:
        instance._previous_account_id = None


@receiver(post_save, sender=Transaction)
def update_account_balance_on_save(sender, instance, **kwargs):
    recalculate_account_balance(instance.account_id)
    previous_account_id = getattr(instance, '_previous_account_id', None)
    if previous_account_id and previous_account_id != instance.account_id:
        recalculate_account_balance(previous_account_id)
    if hasattr(instance, '_previous_account_id'):
        del instance._previous_account_id


@receiver(post_delete, sender=Transaction)
def update_account_balance_on_delete(sender, instance, **kwargs):
    recalculate_account_balance(instance.account_id)
