from django.contrib import admin

from .models import Account
from transactions.models import Transaction


class TransactionInline(admin.TabularInline):
    model = Transaction
    fk_name = 'account'
    extra = 0
    fields = ('transaction_date', 'description', 'type', 'amount')
    readonly_fields = ('transaction_date', 'description', 'type', 'amount')
    show_change_link = True


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'type', 'initial_balance', 'current_balance', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('name', 'user__email')
    ordering = ('name',)
    inlines = [TransactionInline]
