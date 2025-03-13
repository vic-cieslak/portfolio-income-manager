from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from income.models import Income
from portfolio.models import Cryptocurrency, BankAccount
import calendar
from datetime import datetime

@login_required
def dashboard(request):
    current_month = timezone.now().month
    current_year = timezone.now().year

    # Monthly income
    monthly_income = Income.objects.filter(
        date__month=current_month,
        date__year=current_year
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    # Recent income entries
    recent_income = Income.objects.all().order_by('-date')[:5]

    # Portfolio value
    crypto_value = sum(crypto.current_value for crypto in Cryptocurrency.objects.all())
    bank_value = BankAccount.objects.aggregate(Sum('balance'))['balance__sum'] or 0
    total_net_worth = crypto_value + bank_value

    # Income by month for chart
    months = []
    income_data = []

    for month in range(1, 13):
        month_name = calendar.month_name[month]
        months.append(month_name)

        monthly_amount = Income.objects.filter(
            date__month=month,
            date__year=current_year
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        income_data.append(float(monthly_amount))

    # Portfolio allocation for chart
    portfolio_labels = ['Crypto', 'Bank/Cash']
    portfolio_data = [float(crypto_value), float(bank_value)]
    
    # Calculate percentages for display
    total = crypto_value + bank_value
    crypto_percentage = (crypto_value / total * 100) if total > 0 else 0
    bank_percentage = (bank_value / total * 100) if total > 0 else 0

    context = {
        'monthly_income': monthly_income,
        'recent_income': recent_income,
        'total_net_worth': total_net_worth,
        'crypto_value': crypto_value,
        'bank_value': bank_value,
        'crypto_percentage': crypto_percentage,
        'bank_percentage': bank_percentage,
        'months': months,
        'income_data': income_data,
        'portfolio_labels': portfolio_labels,
        'portfolio_data': portfolio_data,
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
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return render(request, 'core/logout.html')