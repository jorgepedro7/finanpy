from django.contrib import admin

from .models import Category
from transactions.models import Transaction


class TransactionInline(admin.TabularInline):
    model = Transaction
    fk_name = 'category'
    extra = 0
    fields = ('transaction_date', 'description', 'type', 'amount', 'account')
    readonly_fields = ('transaction_date', 'description', 'type', 'amount', 'account')
    show_change_link = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'type', 'color', 'created_at')
    list_filter = ('type', 'color')
    search_fields = ('name', 'user__email')
    ordering = ('name',)
    inlines = [TransactionInline]
