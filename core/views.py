from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.views.generic import TemplateView

from accounts.models import Account
from categories.models import Category, CategoryType
from transactions.models import Transaction, TransactionType


class HomeView(TemplateView):
    template_name = 'core/home.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        accounts = Account.objects.filter(user=self.request.user).order_by('name')
        total_balance = accounts.aggregate(
            total=Coalesce(Sum('current_balance'), Decimal('0.00'))
        )['total']
        categories = Category.objects.filter(user=self.request.user).order_by('name')
        category_counts = {
            'income': categories.filter(type=CategoryType.INCOME).count(),
            'expense': categories.filter(type=CategoryType.EXPENSE).count(),
        }
        today = timezone.localdate()
        monthly_transactions = Transaction.objects.filter(
            user=self.request.user,
            transaction_date__year=today.year,
            transaction_date__month=today.month,
        )
        monthly_totals = monthly_transactions.aggregate(
            total_income=Coalesce(
                Sum('amount', filter=Q(type=TransactionType.INCOME)),
                Decimal('0.00'),
            ),
            total_expense=Coalesce(
                Sum('amount', filter=Q(type=TransactionType.EXPENSE)),
                Decimal('0.00'),
            ),
        )
        recent_transactions = (
            Transaction.objects.filter(user=self.request.user)
            .select_related('account', 'category')
            .order_by('-transaction_date', '-created_at')[:10]
        )
        context.update(
            {
                'accounts': accounts,
                'total_balance': total_balance,
                'categories': categories,
                'category_counts': category_counts,
                'recent_transactions': recent_transactions,
                'monthly_income': monthly_totals['total_income'],
                'monthly_expense': monthly_totals['total_expense'],
            }
        )
        return context
