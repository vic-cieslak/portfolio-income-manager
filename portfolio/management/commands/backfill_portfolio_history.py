from django.core.management.base import BaseCommand
from django.utils import timezone
from portfolio.models import PortfolioHistory, Cryptocurrency, BankAccount
from datetime import timedelta
import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Backfills portfolio history with sample data for testing'

    def handle(self, *args, **options):
        # Start from 90 days ago
        start_date = timezone.now().date() - timedelta(days=90)
        
        # Get the latest record (if any)
        latest = PortfolioHistory.objects.first()
        
        if latest:
            crypto_value = latest.crypto_value
            bank_value = latest.bank_value
        else:
            # Default starting values
            crypto_value = Decimal('10000')
            bank_value = Decimal('5000')
        
        # Generate records for each day
        for days in range(90, 0, -1):
            date = start_date + timedelta(days=90-days)
            
            # Skip if record already exists
            if PortfolioHistory.objects.filter(date=date).exists():
                continue
            
            # Add some random fluctuation
            crypto_change = random.uniform(-0.05, 0.05)  # -5% to +5%
            bank_change = random.uniform(-0.01, 0.02)    # -1% to +2%
            
            crypto_value = max(Decimal('0'), crypto_value * (Decimal('1') + Decimal(str(crypto_change))))
            bank_value = max(Decimal('0'), bank_value * (Decimal('1') + Decimal(str(bank_change))))
            
            PortfolioHistory.objects.create(
                date=date,
                crypto_value=crypto_value.quantize(Decimal('0.01')),
                bank_value=bank_value.quantize(Decimal('0.01'))
            )
            
            self.stdout.write(self.style.SUCCESS(f'Created record for {date}'))
        
        # Update Cryptocurrency and BankAccount models with the latest values
        total_crypto_value = crypto_value
        total_bank_value = bank_value

        # Distribute crypto value among existing cryptocurrencies
        cryptocurrencies = Cryptocurrency.objects.all()
        if cryptocurrencies:
            per_crypto_value = total_crypto_value / len(cryptocurrencies)
            for crypto in cryptocurrencies:
                crypto.quantity = per_crypto_value / Decimal('100')  # Assume a price of 100 for simplicity
                crypto.current_price = Decimal('100')
                crypto.save()

        # Distribute bank value among existing bank accounts
        bank_accounts = BankAccount.objects.all()
        if bank_accounts:
            per_account_value = total_bank_value / len(bank_accounts)
            for account in bank_accounts:
                account.balance = per_account_value
                account.save()

        self.stdout.write(self.style.SUCCESS('Portfolio history backfilled successfully'))
