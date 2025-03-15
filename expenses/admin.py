from django.contrib import admin
from .models import Expense, ExpenseCategory

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount', 'date', 'category', 'user')
    list_filter = ('date', 'category', 'user')
    search_fields = ('description', 'category__name', 'user__username')
    date_hierarchy = 'date'

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
