from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from income.models import Income
from expenses.models import Expense
from portfolio.models import Cryptocurrency, BankAccount
import calendar
from datetime import datetime

@login_required
def dashboard(request):
    current_month = timezone.now().month
    current_year = timezone.now().year

    # Monthly income and expenses - using date range for more reliable filtering
    from datetime import datetime, date
    import calendar
    
    # Get the first and last day of the current month
    first_day = date(current_year, current_month, 1)
    last_day = date(current_year, current_month, calendar.monthrange(current_year, current_month)[1])
    
    # Debug information
    print(f"Calculating totals for month: {current_month}/{current_year}")
    print(f"Date range: {first_day} to {last_day}")
    
    # Get monthly income - filter by current user
    monthly_income_queryset = Income.objects.filter(
        user=request.user,
        date__gte=first_day,
        date__lte=last_day
    )
    total_monthly_income = monthly_income_queryset.aggregate(Sum('amount'))['amount__sum'] or 0
    print(f"Found {monthly_income_queryset.count()} income entries for user {request.user.username} this month, total: {total_monthly_income}")
    
    # Get monthly expenses - filter by current user
    monthly_expenses_queryset = Expense.objects.filter(
        user=request.user,
        date__gte=first_day,
        date__lte=last_day
    )
    total_monthly_expenses = monthly_expenses_queryset.aggregate(Sum('amount'))['amount__sum'] or 0
    print(f"Found {monthly_expenses_queryset.count()} expense entries for user {request.user.username} this month, total: {total_monthly_expenses}")

    net_income = total_monthly_income - total_monthly_expenses

    # Recent income and expense entries - filter by current user
    recent_income = Income.objects.filter(user=request.user).order_by('-date')[:5]
    recent_expenses = Expense.objects.filter(user=request.user).order_by('-date')[:5]

    # Portfolio value
    cryptocurrencies = Cryptocurrency.objects.all()
    try:
        # Update crypto prices and record portfolio value
        from portfolio.services import CoinGeckoService
        CoinGeckoService.update_crypto_prices(cryptocurrencies)
        CoinGeckoService.record_portfolio_value()
    except Exception as e:
        messages.warning(request, f"Could not update portfolio data: {str(e)}")
    
    crypto_value = sum(crypto.current_value for crypto in cryptocurrencies)
    bank_value = BankAccount.objects.aggregate(Sum('balance'))['balance__sum'] or 0
    total_net_worth = crypto_value + bank_value

    # Income and expenses by month for chart - using date range for consistency
    months = []
    income_data = []
    expense_data = []

    for month in range(1, 13):
        month_name = calendar.month_name[month]
        months.append(month_name)

        # Get the first and last day of each month
        first_day_of_month = date(current_year, month, 1)
        last_day_of_month = date(current_year, month, calendar.monthrange(current_year, month)[1])

        # Calculate monthly income using date range - filter by current user
        monthly_income = Income.objects.filter(
            user=request.user,
            date__gte=first_day_of_month,
            date__lte=last_day_of_month
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        # Calculate monthly expenses using date range - filter by current user
        monthly_expenses = Expense.objects.filter(
            user=request.user,
            date__gte=first_day_of_month,
            date__lte=last_day_of_month
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        income_data.append(float(monthly_income))
        expense_data.append(float(monthly_expenses))

    # Portfolio allocation for chart
    portfolio_labels = ['Crypto', 'Bank/Cash']
    portfolio_data = [float(crypto_value), float(bank_value)]

    import json


    context = {
        'title': 'Dashboard',
        'monthly_income': total_monthly_income,
        'monthly_expenses': total_monthly_expenses,
        'net_income': net_income,
        'recent_income': recent_income,
        'recent_expenses': recent_expenses,
        'total_net_worth': total_net_worth,
        'crypto_value': crypto_value,
        'bank_value': bank_value,
        'months': json.dumps(months),
        'income_data': json.dumps(income_data),
        'expense_data': json.dumps(expense_data),
        'portfolio_labels': json.dumps(portfolio_labels),
        'portfolio_data': json.dumps(portfolio_data),
    }

    return render(request, 'core/dashboard.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
        'title': 'Login'
    }
    return render(request, 'core/login.html', context)

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    context = {
        'title': 'Logged Out'
    }
    return render(request, 'core/logout.html', context)
