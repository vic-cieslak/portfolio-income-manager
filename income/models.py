
from django.db import models
from django.utils import timezone

class IncomeCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Income Categories'

class Income(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE, related_name='incomes')
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.amount} - {self.date} - {self.category}"
    
    class Meta:
        ordering = ['-date']
