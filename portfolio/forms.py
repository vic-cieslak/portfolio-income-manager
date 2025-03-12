
from django import forms
from .models import Cryptocurrency, BankAccount

class CryptocurrencyForm(forms.ModelForm):
    # Predefined cryptocurrency choices
    CRYPTO_CHOICES = [
        ('bitcoin', 'Bitcoin (BTC)'),
        ('shiba-inu', 'Shiba Inu (SHIB)'),
        ('bonk', 'Bonk (BONK)'),
        ('monero', 'Monero (XMR)'),
    ]
    
    # Override the name field to use choices
    name = forms.ChoiceField(choices=CRYPTO_CHOICES, label="Cryptocurrency")
    
    class Meta:
        model = Cryptocurrency
        fields = ['name', 'symbol', 'quantity', 'acquisition_cost']
        widgets = {
            'acquisition_cost': forms.NumberInput(attrs={'placeholder': 'Optional - Cost Basis'}),
        }

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['name', 'balance']
