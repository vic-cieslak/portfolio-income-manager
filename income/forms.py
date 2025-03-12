
from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .models import Income, IncomeCategory

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'date', 'category', 'description']
        widgets = {
            'date': DatePickerInput(
                options={
                    "format": "YYYY-MM-DD",
                }
            ),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class IncomeCategoryForm(forms.ModelForm):
    class Meta:
        model = IncomeCategory
        fields = ['name']
