
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import requests
from .models import Cryptocurrency, BankAccount
from .forms import CryptocurrencyForm, BankAccountForm
import json

@login_required
def crypto_list(request):
    # Update crypto prices
    update_crypto_prices()
    
    cryptocurrencies = Cryptocurrency.objects.all()
    total_value = sum(crypto.current_value for crypto in cryptocurrencies)
    
    return render(request, 'portfolio/crypto_list.html', {
        'cryptocurrencies': cryptocurrencies,
        'total_value': total_value
    })

@login_required
def crypto_create(request):
    if request.method == 'POST':
        form = CryptocurrencyForm(request.POST)
        if form.is_valid():
            crypto = form.save(commit=False)
            # Get initial price using CoinGecko ID (which is now stored in name field)
            try:
                coin_id = crypto.name  # This is now the CoinGecko ID
                response = requests.get(
                    f'https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd'
                )
                data = response.json()
                if coin_id in data:
                    crypto.current_price = data[coin_id]['usd']
                    crypto.last_updated = timezone.now()
                    
                    # Map the symbol based on the selected cryptocurrency
                    symbols = {
                        'bitcoin': 'BTC',
                        'shiba-inu': 'SHIB',
                        'bonk': 'BONK',
                        'monero': 'XMR'
                    }
                    crypto.symbol = symbols.get(coin_id, crypto.symbol)
            except Exception as e:
                messages.warning(request, f'Could not fetch price: {str(e)}')
            
            crypto.save()
            messages.success(request, 'Cryptocurrency added successfully!')
            return redirect('crypto_list')
    else:
        form = CryptocurrencyForm()
    
    return render(request, 'portfolio/crypto_form.html', {'form': form, 'title': 'Add Cryptocurrency'})

@login_required
def crypto_update(request, pk):
    crypto = get_object_or_404(Cryptocurrency, pk=pk)
    
    if request.method == 'POST':
        form = CryptocurrencyForm(request.POST, instance=crypto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cryptocurrency updated successfully!')
            return redirect('crypto_list')
    else:
        form = CryptocurrencyForm(instance=crypto)
    
    return render(request, 'portfolio/crypto_form.html', {'form': form, 'title': 'Update Cryptocurrency'})

@login_required
def crypto_delete(request, pk):
    crypto = get_object_or_404(Cryptocurrency, pk=pk)
    
    if request.method == 'POST':
        crypto.delete()
        messages.success(request, 'Cryptocurrency deleted successfully!')
        return redirect('crypto_list')
    
    return render(request, 'portfolio/crypto_confirm_delete.html', {'crypto': crypto})

@login_required
def bank_list(request):
    accounts = BankAccount.objects.all()
    total_balance = sum(account.balance for account in accounts)
    
    return render(request, 'portfolio/bank_list.html', {
        'accounts': accounts,
        'total_balance': total_balance
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
    
    return render(request, 'portfolio/bank_form.html', {'form': form, 'title': 'Add Bank Account'})

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
    
    return render(request, 'portfolio/bank_form.html', {'form': form, 'title': 'Update Bank Account'})

@login_required
def bank_delete(request, pk):
    account = get_object_or_404(BankAccount, pk=pk)
    
    if request.method == 'POST':
        account.delete()
        messages.success(request, 'Bank account deleted successfully!')
        return redirect('bank_list')
    
    return render(request, 'portfolio/bank_confirm_delete.html', {'account': account})

def update_crypto_prices():
    """Update cryptocurrency prices from CoinGecko API"""
    cryptocurrencies = Cryptocurrency.objects.all()
    if not cryptocurrencies:
        return
    
    # Get all crypto IDs (name field now contains CoinGecko ID)
    crypto_ids = ",".join([crypto.name for crypto in cryptocurrencies])
    
    try:
        response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_ids}&vs_currencies=usd')
        data = response.json()
        
        for crypto in cryptocurrencies:
            if crypto.name in data:
                crypto.current_price = data[crypto.name]['usd']
                crypto.last_updated = timezone.now()
                crypto.save()
    except Exception as e:
        print(f"Error updating crypto prices: {str(e)}")
