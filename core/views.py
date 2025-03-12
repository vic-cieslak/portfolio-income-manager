
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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
    recent_income = Income.objects.all()[:5]
    
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
    
    context = {
        'monthly_income': monthly_income,
        'recent_income': recent_income,
        'total_net_worth': total_net_worth,
        'crypto_value': crypto_value,
        'bank_value': bank_value,
        'months': months,
        'income_data': income_data,
        'portfolio_labels': portfolio_labels,
        'portfolio_data': portfolio_data,
    }
    
    return render(request, 'core/dashboard.html', context)
