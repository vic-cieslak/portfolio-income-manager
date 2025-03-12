
from django import forms
from .models import Income, IncomeCategory
from bootstrap_datepicker_plus.widgets import DatePickerInput

class IncomeCategoryForm(forms.ModelForm):
    class Meta:
        model = IncomeCategory
        fields = ['name']

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'date', 'category', 'description']
        widgets = {
            'date': DatePickerInput(),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
