from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import CategoryForm
from .models import Category, CategoryType


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'categories/category_list.html'
    context_object_name = 'categories'
    paginate_by = 12

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_categories = Category.objects.filter(user=self.request.user)
        context.update(
            {
                'income_count': user_categories.filter(type=CategoryType.INCOME).count(),
                'expense_count': user_categories.filter(type=CategoryType.EXPENSE).count(),
            }
        )
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('categories:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('categories:list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'categories/category_confirm_delete.html'
    success_url = reverse_lazy('categories:list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
