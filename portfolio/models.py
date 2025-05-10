
from django.db import models
from django.utils import timezone

class PortfolioHistory(models.Model):
    date = models.DateField(default=timezone.now)
    crypto_value = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    bank_value = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Portfolio History'
    
    @property
    def total_value(self):
        return self.crypto_value + self.bank_value

class Cryptocurrency(models.Model):
    # CoinGecko ID (e.g., 'bitcoin', 'ethereum')
    coin_id = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    quantity = models.DecimalField(max_digits=18, decimal_places=8)
    acquisition_cost = models.DecimalField(max_digits=18, decimal_places=10, null=True, blank=True)  # Increased precision
    current_price = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)  # Increased precision
    last_updated = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.symbol} - {self.quantity}"
    
    class Meta:
        verbose_name_plural = 'Cryptocurrencies'
        
    @property
    def current_value(self):
        if self.current_price:
            from decimal import Decimal
            # Convert current_price to Decimal before multiplication
            return self.quantity * Decimal(str(self.current_price))
        return 0

class BankAccount(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.name} - {self.balance}"
