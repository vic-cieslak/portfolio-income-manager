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
import json # Added import for json
from datetime import datetime, timedelta

from .models import Expense, ExpenseCategory
from .forms import ExpenseForm, ExpenseCategoryForm

class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'
    paginate_by = 10

    def get_queryset(self): # Filter expenses by user
        return Expense.objects.filter(user=self.request.user).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Expenses'
        return context

class ExpenseDetailView(LoginRequiredMixin, DetailView):
    model = Expense
    template_name = 'expenses/expense_detail.html'
    context_object_name = 'expense'

    def get_queryset(self): # Filter by user
        return Expense.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Expense: {self.object.description[:20] or self.object.category.name}"
        return context

class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expenses:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Expense'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expenses:list')

    def get_queryset(self): # Filter by user
        return Expense.objects.filter(user=self.request.user)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Edit Expense: {self.object.description[:20] or self.object.category.name}"
        return context

class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'expenses/expense_confirm_delete.html'
    success_url = reverse_lazy('expenses:list')
    
    def get_queryset(self): # Filter by user
        return Expense.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Delete Expense: {self.object.description[:20] or self.object.category.name}"
        return context

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

    month_expenses = Expense.objects.filter(user=request.user, date__gte=start_date, date__lte=end_date)
    total_expense = month_expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    daily_expense = {}
    for expense in month_expenses:
        day = expense.date.day
        daily_expense[day] = daily_expense.get(day, 0) + expense.amount

    # New daily_expense_list for detailed expenses per day (JSON strings)
    expenses_by_day_for_json = {}
    for expense in month_expenses:
        day = expense.date.day
        expense_detail = {
            'category': expense.category.name,
            'amount': str(expense.amount), # Ensure amount is string for JSON
            'description': expense.description or ""
        }
        if day not in expenses_by_day_for_json:
            expenses_by_day_for_json[day] = []
        expenses_by_day_for_json[day].append(expense_detail)

    daily_expense_list_json_strings = {
        day: json.dumps(details) for day, details in expenses_by_day_for_json.items()
    }

    category_breakdown = {}
    for expense in month_expenses:
        category_name = expense.category.name
        category_breakdown[category_name] = category_breakdown.get(category_name, 0) + expense.amount

    calendar_weeks = [[(day, True) if day > 0 else (0, False) for day in week] for week in cal]

    context = {
        'title': f'Expense Calendar - {month_name} {year}',
        'month_days': calendar_weeks,
        'month_name': month_name,
        'year': year,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'daily_expense': daily_expense, # For displaying total in cell
        'daily_expense_list': daily_expense_list_json_strings, # For data-expenses attribute
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
    categories = ExpenseCategory.objects.all() # Removed user filter
    context = {
        'categories': categories,
        'title': 'Expense Categories'
    }
    return render(request, 'expenses/category_list.html', context)

@login_required
def category_create(request):
    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST)
        if form.is_valid():
            # category = form.save(commit=False) # No user to assign
            # category.user = request.user 
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('expenses:category_list')
    else:
        form = ExpenseCategoryForm()
    context = {
        'form': form, 
        'title': 'Add Expense Category'
    }
    return render(request, 'expenses/category_form.html', context)

@login_required
def category_update(request, pk):
    category = get_object_or_404(ExpenseCategory, pk=pk) # Removed user filter

    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('expenses:category_list')
    else:
        form = ExpenseCategoryForm(instance=category)
    context = {
        'form': form, 
        'title': f'Update Expense Category: {category.name}'
    }
    return render(request, 'expenses/category_form.html', context)

@login_required
def category_delete(request, pk):
    category = get_object_or_404(ExpenseCategory, pk=pk) # Removed user filter
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('expenses:category_list')
    context = {
        'category': category,
        'title': f'Delete Expense Category: {category.name}'
    }
    return render(request, 'expenses/category_confirm_delete.html', context)

@login_required
def expense_insights_view(request):
    user = request.user
    now = timezone.now()
    current_year = now.year
    current_month = now.month

    # 1. Total Expenses
    # Current Month
    start_current_month = datetime(current_year, current_month, 1).date()
    end_current_month = (datetime(current_year, current_month + 1, 1) if current_month < 12 else datetime(current_year + 1, 1, 1)).date() - timedelta(days=1)
    total_current_month = Expense.objects.filter(user=user, date__gte=start_current_month, date__lte=end_current_month).aggregate(Sum('amount'))['amount__sum'] or 0

    # Last Month
    if current_month == 1:
        last_month_val, last_month_year = 12, current_year - 1
    else:
        last_month_val, last_month_year = current_month - 1, current_year
    start_last_month = datetime(last_month_year, last_month_val, 1).date()
    end_last_month = datetime(current_year, current_month, 1).date() - timedelta(days=1)
    total_last_month = Expense.objects.filter(user=user, date__gte=start_last_month, date__lte=end_last_month).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Year-to-Date (YTD)
    start_ytd = datetime(current_year, 1, 1).date()
    total_ytd = Expense.objects.filter(user=user, date__gte=start_ytd, date__lte=now.date()).aggregate(Sum('amount'))['amount__sum'] or 0

    # 2. Top 5 Spending Categories (Current Month)
    current_month_expenses = Expense.objects.filter(user=user, date__gte=start_current_month, date__lte=end_current_month)
    category_spending = {}
    for expense in current_month_expenses:
        cat_name = expense.category.name
        category_spending[cat_name] = category_spending.get(cat_name, 0) + expense.amount
    
    top_categories = sorted(category_spending.items(), key=lambda item: item[1], reverse=True)[:5]
    top_categories_labels = [item[0] for item in top_categories]
    top_categories_data = [float(item[1]) for item in top_categories] # Ensure float for Chart.js

    # 3. Monthly Total Expenses (Last 6 Months)
    monthly_totals_data = []
    month_labels = []
    for i in range(5, -1, -1): # Iterate from 5 down to 0 (for last 6 months including current)
        month_offset = current_month - i
        year_offset = current_year
        if month_offset <= 0:
            month_offset += 12
            year_offset -= 1
        
        month_start = datetime(year_offset, month_offset, 1).date()
        month_end = (datetime(year_offset, month_offset + 1, 1) if month_offset < 12 else datetime(year_offset + 1, 1, 1)).date() - timedelta(days=1)
        
        total_for_month = Expense.objects.filter(user=user, date__gte=month_start, date__lte=month_end).aggregate(Sum('amount'))['amount__sum'] or 0
        monthly_totals_data.append(float(total_for_month))
        month_labels.append(calendar.month_abbr[month_offset])

    context = {
        'title': 'Expense Insights',
        'total_current_month': total_current_month,
        'total_last_month': total_last_month,
        'total_ytd': total_ytd,
        'top_categories_labels': json.dumps(top_categories_labels),
        'top_categories_data': json.dumps(top_categories_data),
        'monthly_totals_labels': json.dumps(month_labels),
        'monthly_totals_data': json.dumps(monthly_totals_data),
    }
    return render(request, 'expenses/expense_insights.html', context)
