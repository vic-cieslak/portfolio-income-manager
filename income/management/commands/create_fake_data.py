
import random
from datetime import datetime, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from decimal import Decimal

from income.models import Income, IncomeCategory
from expenses.models import Expense, ExpenseCategory
from portfolio.models import Cryptocurrency, BankAccount

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates fake data for income, expenses, bank accounts, and cryptocurrencies, and creates a superuser'
    
    def get_admin_user(self):
        """Get or create the admin user and return it"""
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            admin_user = User.objects.get(username='admin')
            self.stdout.write(self.style.WARNING('Superuser "admin" already exists'))
        return admin_user

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
        income_categories = ['Salary', 'Freelance', 'Investments', 'Rental', 'Other']
        
        for cat_name in income_categories:
            IncomeCategory.objects.get_or_create(
                name=cat_name,
                defaults={'description': f'Income from {cat_name.lower()}'}
            )
        
        # Create expense categories if they don't exist
        expense_categories = ['Food', 'Housing', 'Transportation', 'Entertainment', 'Utilities', 'Healthcare', 'Shopping']
        
        for cat_name in expense_categories:
            ExpenseCategory.objects.get_or_create(
                name=cat_name,
                defaults={'description': f'Expenses for {cat_name.lower()}'}
            )
        
        # Get all categories
        all_income_categories = IncomeCategory.objects.all()
        all_expense_categories = ExpenseCategory.objects.all()
        
        # Generate entries for the last 90 days
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=90)
        
        # Delete existing data first
        Income.objects.filter(date__gte=start_date, date__lte=end_date).delete()
        Expense.objects.filter(date__gte=start_date, date__lte=end_date).delete()
        
        # Get or create admin user
        admin_user = self.get_admin_user()
        
        # Generate income and expense entries
        current_date = start_date
        while current_date <= end_date:
            # Generate 0-3 income entries per day
            num_income_entries = random.randint(0, 3)
            
            for _ in range(num_income_entries):
                category = random.choice(all_income_categories)
                
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
                    user=admin_user
                )
            
            # Generate 0-4 expense entries per day
            num_expense_entries = random.randint(0, 4)
            
            for _ in range(num_expense_entries):
                category = random.choice(all_expense_categories)
                
                # Generate amount based on category
                if category.name == 'Food':
                    amount = Decimal(str(random.randint(10, 100)))
                elif category.name == 'Housing':
                    amount = Decimal(str(random.randint(200, 1000)))
                elif category.name == 'Transportation':
                    amount = Decimal(str(random.randint(20, 150)))
                elif category.name == 'Entertainment':
                    amount = Decimal(str(random.randint(10, 200)))
                elif category.name == 'Utilities':
                    amount = Decimal(str(random.randint(50, 300)))
                elif category.name == 'Healthcare':
                    amount = Decimal(str(random.randint(20, 500)))
                else:  # Shopping
                    amount = Decimal(str(random.randint(10, 300)))
                
                Expense.objects.create(
                    category=category,
                    amount=amount,
                    date=current_date,
                    description=f'Fake {category.name} expense generated for testing',
                    user=admin_user
                )
            
            current_date += timedelta(days=1)
        
        total_income_created = Income.objects.filter(date__gte=start_date, date__lte=end_date).count()
        total_expense_created = Expense.objects.filter(date__gte=start_date, date__lte=end_date).count()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {total_income_created} fake income entries'))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {total_expense_created} fake expense entries'))

        self.create_fake_bank_accounts()
        self.create_fake_cryptocurrencies()

        bank_accounts_count = BankAccount.objects.count()
        cryptocurrencies_count = Cryptocurrency.objects.count()

        self.stdout.write(self.style.SUCCESS(f'Successfully created {bank_accounts_count} fake bank accounts'))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {cryptocurrencies_count} fake cryptocurrencies'))
