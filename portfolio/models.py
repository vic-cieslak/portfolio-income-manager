
from django.db import models
from django.utils import timezone

class Cryptocurrency(models.Model):
    symbol = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    acquisition_cost = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    current_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.symbol}) - {self.quantity}"
    
    @property
    def current_value(self):
        if self.current_price:
            return self.quantity * self.current_price
        return 0
    
    class Meta:
        verbose_name_plural = "Cryptocurrencies"

class BankAccount(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=20, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.balance}"
