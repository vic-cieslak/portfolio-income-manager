from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Cryptocurrency, BankAccount, PortfolioHistory
from .forms import DateRangeForm, CryptocurrencyForm, BankAccountForm, PortfolioHistoryManualAddForm
from .services import CoinGeckoService
import json
from django.views.decorators.http import require_POST

@login_required
def crypto_list(request):
    cryptocurrencies = Cryptocurrency.objects.all()
    
    try:
        CoinGeckoService.update_crypto_prices(cryptocurrencies)
    except Exception as e:
        messages.warning(request, f"Could not update cryptocurrency prices: {str(e)}")
    
    total_value = sum(crypto.current_value for crypto in cryptocurrencies)
    
    return render(request, 'portfolio/crypto_list.html', {
        'cryptocurrencies': cryptocurrencies,
        'total_value': total_value,
        'title': 'Cryptocurrencies'
    })

@login_required
def crypto_create(request):
    if request.method == 'POST':
        form = CryptocurrencyForm(request.POST)
        if form.is_valid():
            crypto = form.save(commit=False)
            coin_id = form.cleaned_data['coin_id']
            coin_data = CoinGeckoService.get_coin_data(coin_id)
            
            if coin_data:
                crypto.coin_id = coin_data['id']
                crypto.name = coin_data['name']
                crypto.symbol = coin_data['symbol']
                crypto.current_price = coin_data['current_price']
                crypto.last_updated = timezone.now()
                crypto.save()
                
                messages.success(request, 'Cryptocurrency added successfully!')
                return redirect('crypto_list')
            else:
                messages.error(request, 'Could not fetch cryptocurrency data. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CryptocurrencyForm()
    
    return render(request, 'portfolio/crypto_form.html', {
        'form': form,
        'title': 'Add Cryptocurrency'
    })

@login_required
def crypto_update(request, pk):
    crypto = get_object_or_404(Cryptocurrency, pk=pk)
    
    if request.method == 'POST':
        form = CryptocurrencyForm(request.POST, instance=crypto)
        if form.is_valid():
            updated_crypto = form.save(commit=False)
            coin_id = form.cleaned_data['coin_id']
            
            if coin_id != crypto.coin_id:
                coin_data = CoinGeckoService.get_coin_data(coin_id)
                
                if coin_data:
                    updated_crypto.coin_id = coin_data['id']
                    updated_crypto.name = coin_data['name']
                    updated_crypto.symbol = coin_data['symbol']
                    updated_crypto.current_price = coin_data['current_price']
                else:
                    messages.warning(request, 'Could not fetch updated cryptocurrency data, but quantity was updated.')
            
            updated_crypto.last_updated = timezone.now()
            updated_crypto.save()
            messages.success(request, 'Cryptocurrency updated successfully!')
            return redirect('crypto_list')
    else:
        form = CryptocurrencyForm(instance=crypto)
    
    return render(request, 'portfolio/crypto_form.html', {
        'form': form,
        'title': f'Update {crypto.name}'
    })

@login_required
def crypto_delete(request, pk):
    crypto = get_object_or_404(Cryptocurrency, pk=pk)
    
    if request.method == 'POST':
        name = crypto.name
        crypto.delete()
        messages.success(request, f'{name} deleted successfully from your portfolio!')
        return redirect('crypto_list')
    
    return render(request, 'portfolio/crypto_confirm_delete.html', {
        'crypto': crypto,
        'title': f'Delete {crypto.name}'
    })

@login_required
def bank_list(request):
    accounts = BankAccount.objects.all()
    total_balance = sum(account.balance for account in accounts)
    
    return render(request, 'portfolio/bank_list.html', {
        'accounts': accounts,
        'total_balance': total_balance,
        'title': 'Bank Accounts'
    })

@login_required
def bank_create(request):
    if request.method == 'POST':
        form = BankAccountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bank account added successfully!')
            return redirect('bank_list')
    else:
        form = BankAccountForm()
    
    return render(request, 'portfolio/bank_form.html', {
        'form': form,
        'title': 'Add Bank Account'
    })

@login_required
def bank_update(request, pk):
    account = get_object_or_404(BankAccount, pk=pk)
    
    if request.method == 'POST':
        form = BankAccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bank account updated successfully!')
            return redirect('bank_list')
    else:
        form = BankAccountForm(instance=account)
    
    return render(request, 'portfolio/bank_form.html', {
        'form': form,
        'title': f'Update {account.name}'
    })

@login_required
def bank_delete(request, pk):
    account = get_object_or_404(BankAccount, pk=pk)
    
    if request.method == 'POST':
        account.delete()
        messages.success(request, 'Bank account deleted successfully!')
        return redirect('bank_list')
    
    return render(request, 'portfolio/bank_confirm_delete.html', {
        'account': account,
        'title': f'Delete {account.name}'
    })

@login_required
def portfolio_history(request):
    from datetime import timedelta
    
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=90)
    
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['start_date']:
                start_date = form.cleaned_data['start_date']
            if form.cleaned_data['end_date']:
                end_date = form.cleaned_data['end_date']
    else:
        form = DateRangeForm(initial={'start_date': start_date, 'end_date': end_date})
    
    history = PortfolioHistory.objects.filter(
        date__gte=start_date,
        date__lte=end_date
    ).order_by('-date')
    
    dates = []
    crypto_values = []
    bank_values = []
    total_values = []
    
    for record in reversed(history):
        dates.append(record.date.strftime('%Y-%m-%d'))
        crypto_values.append(float(record.crypto_value))
        bank_values.append(float(record.bank_value))
        total_values.append(float(record.total_value))
    
    return render(request, 'portfolio/portfolio_history.html', {
        'form': form,
        'history': history,
        'dates': json.dumps(dates),
        'crypto_values': json.dumps(crypto_values),
        'bank_values': json.dumps(bank_values),
        'total_values': json.dumps(total_values),
        'start_date': start_date,
        'end_date': end_date,
        'title': 'Portfolio History'
    })

@login_required
def add_portfolio_history_manual(request):
    if request.method == 'POST':
        form = PortfolioHistoryManualAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Portfolio history record added successfully.')
            return redirect('portfolio_history')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PortfolioHistoryManualAddForm()
    
    return render(request, 'portfolio/portfolio_history_manual_form.html', {
        'form': form,
        'title': 'Manually Add Portfolio History'
    })

@login_required
@require_POST
def refresh_portfolio_history_today(request):
    target_date = timezone.now().date()
    try:
        _, created = CoinGeckoService.update_or_create_portfolio_history_for_date(target_date)
        if created:
            messages.success(request, f'Portfolio history for {target_date} (Today) created successfully.')
        else:
            messages.success(request, f'Portfolio history for {target_date} (Today) refreshed successfully.')
    except Exception as e:
        messages.error(request, f"Could not refresh portfolio history for today: {str(e)}")
    return redirect('portfolio_history')
