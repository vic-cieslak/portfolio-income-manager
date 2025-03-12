from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
import calendar
from datetime import datetime, timedelta

from .models import Income, IncomeCategory
from .forms import IncomeForm, IncomeCategoryForm #Added import for IncomeCategoryForm


class IncomeListView(LoginRequiredMixin, ListView): #Added LoginRequiredMixin
    model = Income
    template_name = 'income/income_list.html'
    context_object_name = 'incomes'
    paginate_by = 10

class IncomeDetailView(LoginRequiredMixin, DetailView): #Added LoginRequiredMixin
    model = Income
    template_name = 'income/income_detail.html'
    context_object_name = 'income'

class IncomeCreateView(LoginRequiredMixin, CreateView): #Added LoginRequiredMixin
    model = Income
    form_class = IncomeForm
    template_name = 'income/income_form.html'
    success_url = reverse_lazy('income:list')

class IncomeUpdateView(LoginRequiredMixin, UpdateView): #Added LoginRequiredMixin
    model = Income
    form_class = IncomeForm
    template_name = 'income/income_form.html'
    success_url = reverse_lazy('income:list')

class IncomeDeleteView(LoginRequiredMixin, DeleteView): #Added LoginRequiredMixin
    model = Income
    template_name = 'income/income_confirm_delete.html'
    success_url = reverse_lazy('income:list')

def income_calendar(request, year=None, month=None):
    now = timezone.now()
    year = int(year) if year else now.year
    month = int(month) if month else now.month

    # Get calendar matrix for the month
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]

    # Calculate previous and next month
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year

    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    # Get all incomes for this month
    start_date = datetime(year, month, 1).date()
    if month == 12:
        end_date = datetime(year + 1, 1, 1).date() - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1).date() - timedelta(days=1)

    month_incomes = Income.objects.filter(date__gte=start_date, date__lte=end_date)

    # Calculate total income for the month
    total_income = month_incomes.aggregate(Sum('amount'))['amount__sum'] or 0

    # Group incomes by day
    daily_income = {}
    for income in month_incomes:
        day = income.date.day
        if day in daily_income:
            daily_income[day] += income.amount
        else:
            daily_income[day] = income.amount

    # Create category breakdown
    category_breakdown = {}
    for income in month_incomes:
        category_name = income.category.name
        if category_name in category_breakdown:
            category_breakdown[category_name] += income.amount
        else:
            category_breakdown[category_name] = income.amount

    # Prepare calendar data with enhanced structure
    calendar_weeks = []
    for week in cal:
        week_days = []
        for day in week:
            # For each day, add a tuple of (day_number, is_current_month)
            # where is_current_month is always True here because we're using 
            # the built-in calendar module which only gives us days of the current month
            if day > 0:
                week_days.append((day, True))
            else:
                week_days.append((0, False))
        calendar_weeks.append(week_days)

    context = {
        'month_days': calendar_weeks,
        'month_name': month_name,
        'year': year,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'daily_income': daily_income,
        'total_income': total_income,
        'category_breakdown': category_breakdown,
        'month_incomes': month_incomes, #Added this line to keep the original context
    }
    return render(request, 'income/income_calendar.html', context)


@login_required
def category_list(request):
    categories = IncomeCategory.objects.all()
    return render(request, 'income/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = IncomeCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('category_list')
    else:
        form = IncomeCategoryForm()
    
    return render(request, 'income/category_form.html', {'form': form, 'title': 'Add Category'})

@login_required
def category_update(request, pk):
    category = get_object_or_404(IncomeCategory, pk=pk)
    
    if request.method == 'POST':
        form = IncomeCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = IncomeCategoryForm(instance=category)
    
    return render(request, 'income/category_form.html', {'form': form, 'title': 'Update Category'})

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404