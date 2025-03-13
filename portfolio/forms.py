from django import forms
from .models import Cryptocurrency, BankAccount
from .services import CoinGeckoService

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
