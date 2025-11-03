from datetime import date
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import TransactionForm
from .models import Transaction, TransactionType

MONTH_NAMES = {
    1: 'Janeiro',
    2: 'Fevereiro',
    3: 'Março',
    4: 'Abril',
    5: 'Maio',
    6: 'Junho',
    7: 'Julho',
    8: 'Agosto',
    9: 'Setembro',
    10: 'Outubro',
    11: 'Novembro',
    12: 'Dezembro',
}


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 15

    def get_queryset(self):
        queryset = (
            Transaction.objects.filter(user=self.request.user)
            .select_related('account', 'category')
            .order_by('-transaction_date', '-created_at')
        )
        month = self.request.GET.get('month')
        year = self.request.GET.get('year')
        if month and year:
            try:
                month = int(month)
                year = int(year)
                queryset = queryset.filter(transaction_date__year=year, transaction_date__month=month)
            except ValueError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        selected_month = self.request.GET.get('month')
        selected_year = self.request.GET.get('year')
        month = int(selected_month) if selected_month and selected_month.isdigit() else today.month
        year = int(selected_year) if selected_year and selected_year.isdigit() else today.year

        monthly_queryset = (
            Transaction.objects.filter(user=self.request.user, transaction_date__year=year, transaction_date__month=month)
            .select_related('account', 'category')
        )
        totals = monthly_queryset.aggregate(
            total_income=Coalesce(Sum('amount', filter=Q(type=TransactionType.INCOME)), Decimal('0.00')),
            total_expense=Coalesce(Sum('amount', filter=Q(type=TransactionType.EXPENSE)), Decimal('0.00')),
        )
        context.update(
            {
                'month': month,
                'year': year,
                'selected_month': month,
                'selected_year': year,
                'month_options': [(m, MONTH_NAMES[m]) for m in range(1, 13)],
                'year_options': list(range(today.year - 2, today.year + 1)),
                'total_income': totals['total_income'],
                'total_expense': totals['total_expense'],
                'query_string': self._build_query_string(),
            }
        )
        return context

    def _build_query_string(self):
        params = self.request.GET.copy()
        if 'page' in params:
            del params['page']
        return params.urlencode()


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transactions:list')

    def get_initial(self):
        initial = super().get_initial()
        initial.setdefault('transaction_date', date.today())
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transactions:list')

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    success_url = reverse_lazy('transactions:list')

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
