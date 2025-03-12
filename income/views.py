
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
import calendar
from datetime import datetime
from .models import Income, IncomeCategory
from .forms import IncomeForm, IncomeCategoryForm

@login_required
def income_list(request):
    incomes = Income.objects.all()
    return render(request, 'income/income_list.html', {'incomes': incomes})

@login_required
def income_create(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Income added successfully!')
            return redirect('income_list')
    else:
        form = IncomeForm()
    
    return render(request, 'income/income_form.html', {'form': form, 'title': 'Add Income'})

@login_required
def income_update(request, pk):
    income = get_object_or_404(Income, pk=pk)
    
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            messages.success(request, 'Income updated successfully!')
            return redirect('income_list')
    else:
        form = IncomeForm(instance=income)
    
    return render(request, 'income/income_form.html', {'form': form, 'title': 'Update Income'})

@login_required
def income_delete(request, pk):
    income = get_object_or_404(Income, pk=pk)
    
    if request.method == 'POST':
        income.delete()
        messages.success(request, 'Income deleted successfully!')
        return redirect('income_list')
    
    return render(request, 'income/income_confirm_delete.html', {'income': income})

@login_required
def income_calendar(request):
    # Get year and month from request or use current
    year = int(request.GET.get('year', timezone.now().year))
    month = int(request.GET.get('month', timezone.now().month))
    
    # Get all days in month
    num_days = calendar.monthrange(year, month)[1]
    month_name = calendar.month_name[month]
    
    # Get income for each day
    daily_income = {}
    
    for day in range(1, num_days + 1):
        date = datetime(year, month, day).date()
        total = Income.objects.filter(date=date).aggregate(Sum('amount'))['amount__sum'] or 0
        daily_income[day] = total
    
    # Prepare navigation links
    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year = year - 1
    
    next_month = month + 1
    next_year = year
    if next_month > 12:
        next_month = 1
        next_year = year + 1
    
    # Generate month calendar with proper formatting
    cal = calendar.monthcalendar(year, month)
    month_days = []
    
    for week in cal:
        week_days = []
        for day in week:
            # For each day, create a tuple (day_number, is_in_month)
            # 0 means the day doesn't belong to this month
            is_in_month = day != 0
            week_days.append((day, is_in_month))
        month_days.append(week_days)
    
    # Get all income entries for this month for the month_incomes table
    month_incomes = Income.objects.filter(
        date__year=year, 
        date__month=month
    ).order_by('-date')
    
    context = {
        'month_incomes': month_incomes,
        'year': year,
        'month': month,
        'month_name': month_name,
        'num_days': num_days,
        'daily_income': daily_income,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'month_days': month_days,
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
