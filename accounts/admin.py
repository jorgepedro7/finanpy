from django.contrib import admin

from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'type', 'initial_balance', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('name', 'user__email')
    ordering = ('name',)
