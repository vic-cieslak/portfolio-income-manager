
from django import forms
from .models import Cryptocurrency, BankAccount

class CryptocurrencyForm(forms.ModelForm):
    class Meta:
        model = Cryptocurrency
        fields = ['symbol', 'name', 'quantity', 'acquisition_cost']
        widgets = {
            'acquisition_cost': forms.NumberInput(attrs={'placeholder': 'Optional - Cost Basis'}),
        }

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['name', 'balance']
