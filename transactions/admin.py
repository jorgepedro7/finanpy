from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_date', 'description', 'account', 'category', 'type', 'amount')
    list_filter = ('type', 'transaction_date', 'account')
    search_fields = ('description', 'account__name', 'category__name', 'user__email')
    ordering = ('-transaction_date',)
