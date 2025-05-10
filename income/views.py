from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Max
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import calendar
from datetime import datetime, timedelta

from .models import Income, IncomeCategory
from .forms import IncomeForm, IncomeCategoryForm


class IncomeListView(LoginRequiredMixin, ListView): #Added LoginRequiredMixin
    model = Income
    template_name = 'income/income_list.html'
    context_object_name = 'incomes'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get current user
        user = self.request.user
        
        # Get all incomes for the user for efficiency
        all_user_incomes = Income.objects.filter(user=user)
        
        # Get current date info
        today = timezone.now().date()
        current_month_start = today.replace(day=1)
        last_month_end = current_month_start - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)
        year_start = today.replace(month=1, day=1)
        
        # Current month total
        current_month_income = all_user_incomes.filter(
            date__gte=current_month_start,
            date__lte=today
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Previous month total
        previous_month_income = all_user_incomes.filter(
            date__gte=last_month_start,
            date__lte=last_month_end
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Calculate month-over-month change
        if previous_month_income > 0:
            month_change_pct = ((current_month_income - previous_month_income) / previous_month_income) * 100
        else:
            month_change_pct = 100 if current_month_income > 0 else 0
        
        # Year-to-date income
        ytd_income = all_user_incomes.filter(
            date__gte=year_start,
            date__lte=today
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Calculate average monthly income (last 6 months)
        six_months_ago = today.replace(day=1) - timedelta(days=1)
        six_months_ago = six_months_ago.replace(day=1)
        for _ in range(5):  # Go back 5 more months
            six_months_ago = (six_months_ago.replace(day=1) - timedelta(days=1)).replace(day=1)
        
        monthly_incomes = []
        current = six_months_ago
        
        # Get income for each of the last 6 months
        for _ in range(6):
            month_end = (current.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
            month_income = all_user_incomes.filter(
                date__gte=current,
                date__lte=month_end
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            monthly_incomes.append({
                'month': current.strftime('%b'),
                'amount': float(month_income)
            })
            
            current = month_end + timedelta(days=1)
        
        # Calculate average (excluding months with zero income)
        non_zero_months = [m['amount'] for m in monthly_incomes if m['amount'] > 0]
        avg_monthly_income = sum(non_zero_months) / len(non_zero_months) if non_zero_months else 0
        
        # Get income by category
        categories = IncomeCategory.objects.all()
        category_data = []
        
        for category in categories:
            category_sum = all_user_incomes.filter(
                category=category,
                date__gte=current_month_start,
                date__lte=today
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            if category_sum > 0:
                category_data.append({
                    'name': category.name,
                    'amount': float(category_sum)
                })
        
        # Sort categories by amount (descending)
        category_data.sort(key=lambda x: x['amount'], reverse=True)
        
        # Extract month names and amounts into separate lists for the chart
        month_labels = [item['month'] for item in monthly_incomes]
        month_values = [item['amount'] for item in monthly_incomes]
        
        # Convert to JSON for the chart
        import json
        # Ensure we have valid data before converting to JSON
        if month_labels and month_values:
            month_labels_json = json.dumps(month_labels)
            month_values_json = json.dumps(month_values)
        else:
            # Provide empty arrays if no data
            month_labels_json = json.dumps([])
            month_values_json = json.dumps([])
            
        # Add debug info to context
        print(f"DEBUG - Labels: {month_labels}")
        print(f"DEBUG - Values: {month_values}")
        print(f"DEBUG - Labels JSON: {month_labels_json}")
        print(f"DEBUG - Values JSON: {month_values_json}")
        
        # Get current week (Monday to Sunday)
        today = timezone.now().date()
        current_week_start = today - timedelta(days=today.weekday())  # Monday
        current_week_end = current_week_start + timedelta(days=6)  # Sunday

        # Get last week
        last_week_start = current_week_start - timedelta(days=7)
        last_week_end = current_week_end - timedelta(days=7)

        # Current week total
        current_week_income = all_user_incomes.filter(
            date__gte=current_week_start,
            date__lte=current_week_end
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        # Last week total
        last_week_income = all_user_incomes.filter(
            date__gte=last_week_start,
            date__lte=last_week_end
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        # --- New Stats: Working Days & ADR ---
        total_income_all_time = all_user_incomes.aggregate(Sum('amount'))['amount__sum'] or 0
        total_working_days = all_user_incomes.values('date').distinct().count()
        average_daily_rate = total_income_all_time / total_working_days if total_working_days > 0 else 0

        # --- New Stats: Highest Income Days ---
        # Highest income day - Current Week
        top_day_week_data = all_user_incomes.filter(
            date__gte=current_week_start, date__lte=current_week_end
        ).values('date').annotate(daily_sum=Sum('amount')).order_by('-daily_sum').first()
        
        # Highest income day - Current Month
        top_day_month_data = all_user_incomes.filter(
            date__gte=current_month_start, date__lte=today
        ).values('date').annotate(daily_sum=Sum('amount')).order_by('-daily_sum').first()

        # Highest income day - Current Year
        top_day_year_data = all_user_incomes.filter(
            date__gte=year_start, date__lte=today
        ).values('date').annotate(daily_sum=Sum('amount')).order_by('-daily_sum').first()

        # Add all data to context
        context.update({
            'current_month_income': current_month_income,
            'previous_month_income': previous_month_income,
            'month_change_pct': month_change_pct,
            'ytd_income': ytd_income,
            'avg_monthly_income': avg_monthly_income,
            'category_data': category_data,
            'monthly_income_data': monthly_incomes,
            'month_labels': month_labels,
            'month_values': month_values,
            'month_labels_json': month_labels_json,
            'month_values_json': month_values_json,
            'today': today,
            'current_week_income': current_week_income,
            'last_week_income': last_week_income,
            'current_week_start': current_week_start,
            'current_week_end': current_week_end,
            'last_week_start': last_week_start,
            'last_week_end': last_week_end,
            # New stats
            'total_working_days': total_working_days,
            'average_daily_rate': average_daily_rate,
            'top_day_week_data': top_day_week_data,
            'top_day_month_data': top_day_month_data,
            'top_day_year_data': top_day_year_data,
        })
        
        return context

class IncomeDetailView(LoginRequiredMixin, DetailView): #Added LoginRequiredMixin
    model = Income
    template_name = 'income/income_detail.html'
    context_object_name = 'income'

class IncomeCreateView(LoginRequiredMixin, CreateView): #Added LoginRequiredMixin
    model = Income
    form_class = IncomeForm
    template_name = 'income/income_form.html'
    success_url = reverse_lazy('income:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

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
            
    # Convert dictionary to list for template access (no need for get_item filter)
    daily_income_list = [(day, amount) for day, amount in daily_income.items()]

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
        'daily_income_list': daily_income_list,
        'total_income': total_income,
        'category_breakdown': category_breakdown,
        'month_incomes': month_incomes,
    }
    return render(request, 'income/income_calendar.html', context)

@login_required
@require_POST
def update_income_ajax(request):
    income_id = request.POST.get('income_id')
    new_amount = request.POST.get('amount')
    new_date = request.POST.get('date')
    new_description = request.POST.get('description', '')

    try:
        # Try to get the income object with user filter
        income = Income.objects.get(id=income_id, user=request.user)
    except Income.DoesNotExist:
        try:
            # If not found, try without user filter (for backward compatibility)
            income = Income.objects.get(id=income_id)
            # Assign the current user to the income object
            income.user = request.user
        except Income.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Income not found'}, status=404)
    
    try:
        income.amount = float(new_amount)
        income.date = datetime.strptime(new_date, '%Y-%m-%d').date()
        income.description = new_description
        income.save()
        return JsonResponse({
            'success': True,
            'id': income.id,
            'amount': str(income.amount),
            'date': income.date.strftime('%Y-%m-%d'),
            'description': income.description
        })
    except ValueError as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'An unexpected error occurred'}, status=500)


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
            return redirect('income:category_list')
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
            return redirect('income:category_list')
    else:
        form = IncomeCategoryForm(instance=category)

    return render(request, 'income/category_form.html', {'form': form, 'title': 'Update Category'})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(IncomeCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('income:category_list')
    return render(request, 'income/category_confirm_delete.html', {'category': category})
