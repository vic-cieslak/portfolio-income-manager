
import random
from datetime import datetime, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from decimal import Decimal

from income.models import Income, IncomeCategory
from portfolio.models import Cryptocurrency, BankAccount

User = get_user_model()

def get_default_user():
    User = get_user_model()
    user, created = User.objects.get_or_create(
        username='default_user',
        defaults={'email': 'default@example.com'}
    )
    return user

class Command(BaseCommand):
    help = 'Creates fake data for income, bank accounts, and cryptocurrencies, and creates a superuser'
    
    def create_superuser(self):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Superuser "admin" already exists'))

    def create_fake_bank_accounts(self):
        bank_names = ['Checking Account', 'Savings Account', 'Investment Account', 'Emergency Fund', 'Vacation Savings']
        for _ in range(random.randint(3, 5)):
            name = random.choice(bank_names)
            balance = Decimal(str(random.uniform(100, 10000))).quantize(Decimal('0.01'))
            BankAccount.objects.create(
                name=name,
                balance=balance,
                description=f'Fake {name} generated for testing'
            )

    def create_fake_cryptocurrencies(self):
        crypto_data = [
            ('bitcoin', 'Bitcoin', 'BTC'),
            ('ethereum', 'Ethereum', 'ETH'),
            ('cardano', 'Cardano', 'ADA'),
            ('dogecoin', 'Dogecoin', 'DOGE'),
            ('polkadot', 'Polkadot', 'DOT')
        ]
        for coin_id, name, symbol in crypto_data:
            quantity = Decimal(str(random.uniform(0.1, 10))).quantize(Decimal('0.00000001'))
            current_price = Decimal(str(random.uniform(10, 50000))).quantize(Decimal('0.01'))
            Cryptocurrency.objects.create(
                coin_id=coin_id,
                name=name,
                symbol=symbol,
                quantity=quantity,
                current_price=current_price,
                acquisition_cost=current_price * quantity
            )

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating fake data...')
        
        # Create income categories if they don't exist
        categories = ['Salary', 'Freelance', 'Investments', 'Rental', 'Other']
        
        for cat_name in categories:
            IncomeCategory.objects.get_or_create(
                name=cat_name,
                defaults={'description': f'Income from {cat_name.lower()}'}
            )
        
        # Get all categories
        all_categories = IncomeCategory.objects.all()
        
        # Generate income entries for the last 90 days
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=90)
        
        # Delete existing data first
        Income.objects.filter(date__gte=start_date, date__lte=end_date).delete()
        
        default_user = get_default_user()
        
        current_date = start_date
        while current_date <= end_date:
            # Generate 0-3 income entries per day
            num_entries = random.randint(0, 3)
            
            for _ in range(num_entries):
                category = random.choice(all_categories)
                
                # Generate amount based on category
                if category.name == 'Salary':
                    amount = Decimal(str(random.randint(100, 500)))
                elif category.name == 'Freelance':
                    amount = Decimal(str(random.randint(50, 300)))
                elif category.name == 'Investments':
                    amount = Decimal(str(random.randint(10, 200)))
                elif category.name == 'Rental':
                    amount = Decimal(str(random.randint(300, 800)))
                else:
                    amount = Decimal(str(random.randint(5, 100)))
                
                Income.objects.create(
                    category=category,
                    amount=amount,
                    date=current_date,
                    description=f'Fake {category.name} income generated for testing',
                    user=default_user
                )
            
            current_date += timedelta(days=1)
        
        total_created = Income.objects.filter(date__gte=start_date, date__lte=end_date).count()
        self.stdout.write(self.style.SUCCESS(f'Successfully created {total_created} fake income entries'))

        self.create_fake_bank_accounts()
        self.create_fake_cryptocurrencies()

        bank_accounts_count = BankAccount.objects.count()
        cryptocurrencies_count = Cryptocurrency.objects.count()

        self.stdout.write(self.style.SUCCESS(f'Successfully created {bank_accounts_count} fake bank accounts'))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {cryptocurrencies_count} fake cryptocurrencies'))

        self.create_superuser()
