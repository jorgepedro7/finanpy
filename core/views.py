from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.views.generic import TemplateView

from accounts.models import Account


class HomeView(TemplateView):
    template_name = 'core/home.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        accounts = Account.objects.filter(user=self.request.user).order_by('name')
        total_balance = accounts.aggregate(
            total=Coalesce(Sum('initial_balance'), Decimal('0.00'))
        )['total']
        context.update(
            {
                'accounts': accounts,
                'total_balance': total_balance,
            }
        )
        return context
