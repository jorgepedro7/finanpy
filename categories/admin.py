from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'type', 'color', 'created_at')
    list_filter = ('type', 'color')
    search_fields = ('name', 'user__email')
    ordering = ('name',)
