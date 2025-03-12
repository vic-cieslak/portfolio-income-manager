
from django import forms
from .models import Cryptocurrency, BankAccount

class CryptocurrencyForm(forms.ModelForm):
    class Meta:
        model = Cryptocurrency
        fields = ['name', 'symbol', 'quantity', 'acquisition_cost']

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['name', 'balance']
