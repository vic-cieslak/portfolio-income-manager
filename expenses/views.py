from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import calendar
from datetime import datetime, timedelta

from .models import Expense, ExpenseCategory
from .forms import ExpenseForm, ExpenseCategoryForm

class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'
    paginate_by = 10

class ExpenseDetailView(LoginRequiredMixin, DetailView):
    model = Expense
    template_name = 'expenses/expense_detail.html'
    context_object_name = 'expense'

class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expenses:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expenses:list')

class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'expenses/expense_confirm_delete.html'
    success_url = reverse_lazy('expenses:list')

@login_required
def expense_calendar(request, year=None, month=None):
    now = timezone.now()
    year = int(year) if year else now.year
    month = int(month) if month else now.month

    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]

    if month == 1:
        prev_month, prev_year = 12, year - 1
    else:
        prev_month, prev_year = month - 1, year

    if month == 12:
        next_month, next_year = 1, year + 1
    else:
        next_month, next_year = month + 1, year

    start_date = datetime(year, month, 1).date()
    end_date = (datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)).date() - timedelta(days=1)

    month_expenses = Expense.objects.filter(date__gte=start_date, date__lte=end_date)
    total_expense = month_expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    daily_expense = {}
    for expense in month_expenses:
        day = expense.date.day
        daily_expense[day] = daily_expense.get(day, 0) + expense.amount

    daily_expense_list = [(day, amount) for day, amount in daily_expense.items()]

    category_breakdown = {}
    for expense in month_expenses:
        category_name = expense.category.name
        category_breakdown[category_name] = category_breakdown.get(category_name, 0) + expense.amount

    calendar_weeks = [[(day, True) if day > 0 else (0, False) for day in week] for week in cal]

    context = {
        'month_days': calendar_weeks,
        'month_name': month_name,
        'year': year,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'daily_expense': daily_expense,
        'daily_expense_list': daily_expense_list,
        'total_expense': total_expense,
        'category_breakdown': category_breakdown,
        'month_expenses': month_expenses,
    }
    return render(request, 'expenses/expense_calendar.html', context)

@login_required
@require_POST
def update_expense_ajax(request):
    expense_id = request.POST.get('expense_id')
    new_amount = request.POST.get('amount')
    new_date = request.POST.get('date')
    new_description = request.POST.get('description', '')

    try:
        expense = Expense.objects.get(id=expense_id, user=request.user)
    except Expense.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Expense not found'}, status=404)
    
    try:
        expense.amount = float(new_amount)
        expense.date = datetime.strptime(new_date, '%Y-%m-%d').date()
        expense.description = new_description
        expense.save()
        return JsonResponse({
            'success': True,
            'id': expense.id,
            'amount': str(expense.amount),
            'date': expense.date.strftime('%Y-%m-%d'),
            'description': expense.description
        })
    except ValueError as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'An unexpected error occurred'}, status=500)

@login_required
def category_list(request):
    categories = ExpenseCategory.objects.all()
    return render(request, 'expenses/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('expenses:category_list')
    else:
        form = ExpenseCategoryForm()

    return render(request, 'expenses/category_form.html', {'form': form, 'title': 'Add Category'})

@login_required
def category_update(request, pk):
    category = get_object_or_404(ExpenseCategory, pk=pk)

    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('expenses:category_list')
    else:
        form = ExpenseCategoryForm(instance=category)

    return render(request, 'expenses/category_form.html', {'form': form, 'title': 'Update Category'})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(ExpenseCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('expenses:category_list')
    return render(request, 'expenses/category_confirm_delete.html', {'category': category})
