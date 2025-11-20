from datetime import date, datetime
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce, TruncMonth
from django.utils import timezone
from django.urls import reverse
from django.views.generic import TemplateView, View

import csv

from accounts.models import Account, AccountType
from categories.models import Category, CategoryType
from transactions.models import Transaction, TransactionType

TAILWIND_TO_HEX = {
    'bg-indigo-500': '#6366F1',
    'bg-blue-500': '#3B82F6',
    'bg-purple-500': '#8B5CF6',
    'bg-green-500': '#22C55E',
    'bg-emerald-500': '#10B981',
    'bg-amber-500': '#F59E0B',
    'bg-pink-500': '#EC4899',
    'bg-red-500': '#EF4444',
}

FALLBACK_COLORS = [
    '#6366F1',
    '#3B82F6',
    '#8B5CF6',
    '#22C55E',
    '#10B981',
    '#F59E0B',
    '#EC4899',
    '#EF4444',
]

MONTH_LABELS = [
    'Jan',
    'Fev',
    'Mar',
    'Abr',
    'Mai',
    'Jun',
    'Jul',
    'Ago',
    'Set',
    'Out',
    'Nov',
    'Dez',
]

EXPENSE_TARGET_RATIO = Decimal('0.80')


def resolve_chart_color(tailwind_class, index):
    color = None
    if tailwind_class:
        color = TAILWIND_TO_HEX.get(tailwind_class)
    if not color:
        color = FALLBACK_COLORS[index % len(FALLBACK_COLORS)]
    return color


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
        monthly_net_balance = (
            monthly_totals['total_income'] - monthly_totals['total_expense']
        )
        recent_transactions = (
            Transaction.objects.filter(user=self.request.user)
            .select_related('account', 'category')
            .order_by('-transaction_date', '-created_at')[:10]
        )
        expense_by_category = (
            monthly_transactions.filter(type=TransactionType.EXPENSE)
            .values('category__name', 'category__color')
            .annotate(
                total=Coalesce(Sum('amount'), Decimal('0.00')),
            )
            .order_by('-total')
        )
        category_labels = []
        category_values = []
        category_colors = []
        for index, item in enumerate(expense_by_category):
            total = item['total']
            if total <= 0:
                continue
            category_labels.append(item['category__name'] or 'Sem categoria')
            category_values.append(float(total))
            category_colors.append(resolve_chart_color(item['category__color'], index))
        account_labels = []
        account_balances = []
        for account in accounts:
            account_labels.append(account.name)
            account_balances.append(float(account.current_balance))
        current_month_start = today.replace(day=1)
        month_starts = []
        year_cursor = current_month_start.year
        month_cursor = current_month_start.month
        for _ in range(6):
            month_starts.append(date(year_cursor, month_cursor, 1))
            month_cursor -= 1
            if month_cursor == 0:
                month_cursor = 12
                year_cursor -= 1
        month_starts.sort()
        monthly_series = (
            Transaction.objects.filter(
                user=self.request.user,
                transaction_date__gte=month_starts[0],
            )
            .annotate(month=TruncMonth('transaction_date'))
            .values('month')
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
            .order_by('month')
        )
        monthly_income_points = []
        monthly_expense_points = []
        monthly_target_points = []
        month_labels = []
        series_map = {}
        for item in monthly_series:
            month_value = item['month']
            if isinstance(month_value, datetime):
                month_key = month_value.date()
            elif isinstance(month_value, date):
                month_key = month_value
            else:
                month_key = datetime.strptime(str(month_value), '%Y-%m-%d').date()
            series_map[month_key] = item
        for month_start in month_starts:
            summary = series_map.get(month_start, None)
            income_value = summary['total_income'] if summary else Decimal('0.00')
            expense_value = summary['total_expense'] if summary else Decimal('0.00')
            target_value = income_value * EXPENSE_TARGET_RATIO
            month_labels.append(f"{MONTH_LABELS[month_start.month - 1]}/{month_start.year}")
            monthly_income_points.append(float(income_value))
            monthly_expense_points.append(float(expense_value))
            monthly_target_points.append(float(target_value))
        context.update(
            {
                'accounts': accounts,
                'total_balance': total_balance,
                'categories': categories,
                'category_counts': category_counts,
                'recent_transactions': recent_transactions,
                'monthly_income': monthly_totals['total_income'],
                'monthly_expense': monthly_totals['total_expense'],
                'monthly_net_balance': monthly_net_balance,
                'dashboard_category_chart': {
                    'labels': category_labels,
                    'values': category_values,
                    'colors': category_colors,
                },
                'dashboard_account_chart': {
                    'labels': account_labels,
                    'balances': account_balances,
                },
                'dashboard_monthly_chart': {
                    'labels': month_labels,
                    'income': monthly_income_points,
                    'expense': monthly_expense_points,
                    'target': monthly_target_points,
                },
            }
        )
        return context


class ReportDataMixin:
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

    def get_transactions_queryset(self, start_date, end_date):
        return (
            Transaction.objects.filter(
                user=self.request.user,
                transaction_date__range=(start_date, end_date),
            )
            .select_related('account', 'category')
        )

    def get_summary_totals(self, transactions):
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
        return summary, balance

    def build_category_summary(self, transactions):
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
        category_type_map = dict(CategoryType.choices)
        category_summary = []
        for index, item in enumerate(raw_category_summary):
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
                    'chart_color': resolve_chart_color(item['category__color'], index),
                }
            )
        return category_summary

    def build_account_summary(self, transactions):
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
        account_type_map = dict(AccountType.choices)
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
        return account_summary

    def build_chart_payloads(self, category_summary, account_summary):
        category_chart_data = {
            'labels': [],
            'income': [],
            'expense': [],
            'colors': [],
        }
        for item in category_summary:
            if item['income'] > 0 or item['expense'] > 0:
                category_chart_data['labels'].append(item['name'])
                category_chart_data['income'].append(float(item['income']))
                category_chart_data['expense'].append(float(item['expense']))
                category_chart_data['colors'].append(item['chart_color'])

        account_chart_data = {
            'labels': [],
            'income': [],
            'expense': [],
            'balance': [],
        }
        for item in account_summary:
            if item['income'] > 0 or item['expense'] > 0:
                account_chart_data['labels'].append(item['name'])
                account_chart_data['income'].append(float(item['income']))
                account_chart_data['expense'].append(float(item['expense']))
                account_chart_data['balance'].append(float(item['balance']))
        return category_chart_data, account_chart_data


class ReportsView(LoginRequiredMixin, ReportDataMixin, TemplateView):
    template_name = 'core/reports.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date, end_date = self.get_date_range()

        transactions = self.get_transactions_queryset(start_date, end_date)
        summary, balance = self.get_summary_totals(transactions)
        category_summary = self.build_category_summary(transactions)
        account_summary = self.build_account_summary(transactions)
        category_chart_data, account_chart_data = self.build_chart_payloads(
            category_summary, account_summary
        )
        export_url = reverse('reports_export')
        if self.request.GET:
            export_url = f'{export_url}?{self.request.GET.urlencode()}'

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
                'reports_category_chart': category_chart_data,
                'reports_account_chart': account_chart_data,
                'export_url': export_url,
            }
        )
        return context


class ReportsExportView(LoginRequiredMixin, ReportDataMixin, View):
    def get(self, request, *args, **kwargs):
        start_date, end_date = self.get_date_range()
        transactions = self.get_transactions_queryset(start_date, end_date)
        summary, balance = self.get_summary_totals(transactions)
        category_summary = self.build_category_summary(transactions)
        account_summary = self.build_account_summary(transactions)

        response = HttpResponse(content_type='text/csv')
        filename = f'relatorio-financeiro-{start_date.strftime("%Y%m%d")}-{end_date.strftime("%Y%m%d")}.csv'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response, delimiter=';')
        writer.writerow(['Resumo', f'Período {start_date:%d/%m/%Y} - {end_date:%d/%m/%Y}', '', '', '', ''])
        writer.writerow(
            [
                '',
                '',
                '',
                f'Receitas: {summary["total_income"]:.2f}',
                f'Despesas: {summary["total_expense"]:.2f}',
                f'Saldo: {balance:.2f}',
            ]
        )
        writer.writerow([])
        writer.writerow(['Seção', 'Nome', 'Tipo', 'Receitas', 'Despesas', 'Saldo'])

        for item in category_summary:
            writer.writerow(
                [
                    'Categoria',
                    item['name'],
                    item['type_label'],
                    f'{item["income"]:.2f}',
                    f'{item["expense"]:.2f}',
                    f'{item["balance"]:.2f}',
                ]
            )

        if category_summary:
            writer.writerow([])

        for item in account_summary:
            writer.writerow(
                [
                    'Conta',
                    item['name'],
                    item['type_label'],
                    f'{item["income"]:.2f}',
                    f'{item["expense"]:.2f}',
                    f'{item["balance"]:.2f}',
                ]
            )

        if not category_summary and not account_summary:
            writer.writerow(['Sem dados', 'Não há movimentações no período filtrado', '', '', '', ''])

        return response
