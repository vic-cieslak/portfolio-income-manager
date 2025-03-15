from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .models import Expense, ExpenseCategory

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'date', 'category', 'description']
        widgets = {
            'date': DatePickerInput(
                options={
                    "format": "YYYY-MM-DD",
                }
            ),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ['name', 'description']
