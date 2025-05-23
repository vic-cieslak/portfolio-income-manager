from django import forms
from .models import Cryptocurrency, BankAccount, PortfolioHistory
from .services import CoinGeckoService
from django.utils import timezone

class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        label="Start Date"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        label="End Date"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after start date")
        
        return cleaned_data

class CryptocurrencyForm(forms.ModelForm):
    # This will be populated dynamically
    coin_id = forms.ChoiceField(choices=[], label="Cryptocurrency")
    
    class Meta:
        model = Cryptocurrency
        fields = ['coin_id', 'quantity', 'acquisition_cost']
        widgets = {
            'acquisition_cost': forms.NumberInput(attrs={'placeholder': 'Optional - Cost Basis'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get cryptocurrency choices from CoinGecko API
        choices = CoinGeckoService.get_top_cryptocurrencies()
        
        # If API fails, provide a fallback
        if not choices:
            choices = [
                ('bitcoin', 'Bitcoin (BTC)'),
                ('ethereum', 'Ethereum (ETH)'),
                ('tether', 'Tether (USDT)'),
                ('binancecoin', 'Binance Coin (BNB)'),
            ]
        
        self.fields['coin_id'].choices = choices
        
        # If editing an existing cryptocurrency, set the initial value
        if self.instance and self.instance.pk and self.instance.coin_id:
            self.fields['coin_id'].initial = self.instance.coin_id

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['name', 'balance']

class PortfolioHistoryManualAddForm(forms.ModelForm):
    class Meta:
        model = PortfolioHistory
        fields = ['date', 'crypto_value', 'bank_value']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'crypto_value': forms.NumberInput(attrs={'class': 'form-control'}),
            'bank_value': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if PortfolioHistory.objects.filter(date=date).exists():
            raise forms.ValidationError("A history record for this date already exists. Please use the 'refresh' functionality or edit if available.")
        if date and date > timezone.now().date():
            raise forms.ValidationError("Cannot add history for a future date.")
        return date
