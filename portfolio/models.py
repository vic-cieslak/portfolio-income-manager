
from django.db import models
from django.utils import timezone

class Cryptocurrency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    quantity = models.DecimalField(max_digits=18, decimal_places=8)
    acquisition_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_price = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    last_updated = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.symbol} - {self.quantity}"
    
    class Meta:
        verbose_name_plural = 'Cryptocurrencies'
        
    @property
    def current_value(self):
        if self.current_price:
            return self.quantity * self.current_price
        return 0

class BankAccount(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.name} - {self.balance}"
