from decimal import Decimal
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.views.generic import TemplateView

from accounts.models import Account, AccountType
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


class ReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'core/reports.html'

    def get_date_range(self):
        today = timezone.localdate()
        start_default = today.replace(day=1)
        end_default = today
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')
        date_format = '%Y-%m-%d'

        start_date = start_default
        end_date = end_default

        if data_inicio:
            try:
                start_date = datetime.strptime(data_inicio, date_format).date()
            except ValueError:
                pass
        if data_fim:
            try:
                end_date = datetime.strptime(data_fim, date_format).date()
            except ValueError:
                pass

        if start_date > end_date:
            start_date, end_date = end_date, start_date

        return start_date, end_date

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date, end_date = self.get_date_range()

        transactions = (
            Transaction.objects.filter(
                user=self.request.user,
                transaction_date__range=(start_date, end_date),
            )
            .select_related('account', 'category')
        )

        summary = transactions.aggregate(
            total_income=Coalesce(
                Sum('amount', filter=Q(type=TransactionType.INCOME)),
                Decimal('0.00'),
            ),
            total_expense=Coalesce(
                Sum('amount', filter=Q(type=TransactionType.EXPENSE)),
                Decimal('0.00'),
            ),
        )
        balance = summary['total_income'] - summary['total_expense']

        raw_category_summary = (
            transactions.values(
                'category__id',
                'category__name',
                'category__color',
                'category__type',
            )
            .annotate(
                total_income=Coalesce(
                    Sum('amount', filter=Q(type=TransactionType.INCOME)),
                    Decimal('0.00'),
                ),
                total_expense=Coalesce(
                    Sum('amount', filter=Q(type=TransactionType.EXPENSE)),
                    Decimal('0.00'),
                ),
            )
            .order_by('-total_income', '-total_expense')
        )

        raw_account_summary = (
            transactions.values(
                'account__id',
                'account__name',
                'account__type',
            )
            .annotate(
                total_income=Coalesce(
                    Sum('amount', filter=Q(type=TransactionType.INCOME)),
                    Decimal('0.00'),
                ),
                total_expense=Coalesce(
                    Sum('amount', filter=Q(type=TransactionType.EXPENSE)),
                    Decimal('0.00'),
                ),
            )
            .order_by('account__name')
        )

        category_type_map = dict(CategoryType.choices)
        account_type_map = dict(AccountType.choices)

        category_summary = []
        for item in raw_category_summary:
            income = item['total_income']
            expense = item['total_expense']
            category_summary.append(
                {
                    'name': item['category__name'] or 'Sem categoria',
                    'type_label': category_type_map.get(item['category__type'], 'Não classificada'),
                    'color_class': item['category__color'],
                    'income': income,
                    'expense': expense,
                    'balance': income - expense,
                }
            )

        account_summary = []
        for item in raw_account_summary:
            income = item['total_income']
            expense = item['total_expense']
            account_summary.append(
                {
                    'name': item['account__name'],
                    'type_label': account_type_map.get(item['account__type'], 'Conta'),
                    'income': income,
                    'expense': expense,
                    'balance': income - expense,
                }
            )

        context.update(
            {
                'data_inicio': start_date.isoformat(),
                'data_fim': end_date.isoformat(),
                'total_income': summary['total_income'],
                'total_expense': summary['total_expense'],
                'balance': balance,
                'category_summary': category_summary,
                'account_summary': account_summary,
                'has_transactions': transactions.exists(),
            }
        )
        return context
