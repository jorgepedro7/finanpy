from decimal import Decimal

from django.db import migrations, models
from django.db.models import F


def copy_initial_to_current(apps, schema_editor):
    Account = apps.get_model('accounts', 'Account')
    Account.objects.all().update(current_balance=F('initial_balance'))


def reset_current_balance(apps, schema_editor):
    Account = apps.get_model('accounts', 'Account')
    Account.objects.all().update(current_balance=Decimal('0.00'))


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='current_balance',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12),
        ),
        migrations.RunPython(copy_initial_to_current, reset_current_balance),
    ]
