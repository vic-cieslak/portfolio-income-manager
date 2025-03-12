
import random
from datetime import datetime, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from income.models import Income, IncomeCategory
from portfolio.models import Asset, AssetCategory, Transaction

class Command(BaseCommand):
    help = 'Creates fake data for the application'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating fake data...')
        
        # Create income categories
        income_categories = [
            {'name': 'Salary', 'description': 'Monthly salary income'},
            {'name': 'Freelance', 'description': 'Freelance project income'},
            {'name': 'Dividends', 'description': 'Dividend payments from investments'},
            {'name': 'Interest', 'description': 'Interest earned from savings accounts'},
            {'name': 'Rental', 'description': 'Income from rental properties'},
        ]
        
        for category in income_categories:
            IncomeCategory.objects.get_or_create(
                name=category['name'],
                defaults={'description': category['description']}
            )
        self.stdout.write(self.style.SUCCESS(f'Created {len(income_categories)} income categories'))
        
        # Create income entries (3 months of data)
        income_categories = IncomeCategory.objects.all()
        income_entries = []
        
        # Start date 3 months ago
        start_date = timezone.now().date() - timedelta(days=90)
        
        # Generate income for each day with some randomness (30% chance of income on a given day)
        for i in range(90):
            current_date = start_date + timedelta(days=i)
            if random.random() < 0.3:  # 30% chance of income on a given day
                for _ in range(random.randint(1, 3)):  # 1-3 income entries per day
                    category = random.choice(income_categories)
                    
                    # Amount based on category
                    if category.name == 'Salary':
                        amount = Decimal(random.randint(2000, 5000))
                    elif category.name == 'Freelance':
                        amount = Decimal(random.randint(200, 1500))
                    elif category.name == 'Dividends':
                        amount = Decimal(random.randint(50, 500))
                    elif category.name == 'Interest':
                        amount = Decimal(random.randint(10, 100))
                    elif category.name == 'Rental':
                        amount = Decimal(random.randint(800, 2000))
                    else:
                        amount = Decimal(random.randint(50, 1000))
                    
                    description = f"Sample {category.name.lower()} income for {current_date.strftime('%B %d')}"
                    
                    income_entries.append(Income(
                        amount=amount,
                        date=current_date,
                        category=category,
                        description=description
                    ))
        
        # Bulk create income entries
        Income.objects.bulk_create(income_entries)
        self.stdout.write(self.style.SUCCESS(f'Created {len(income_entries)} income entries'))
        
        # Create asset categories
        asset_categories = [
            {'name': 'Stocks', 'description': 'Individual company stocks'},
            {'name': 'ETFs', 'description': 'Exchange-traded funds'},
            {'name': 'Bonds', 'description': 'Government and corporate bonds'},
            {'name': 'Real Estate', 'description': 'Property investments'},
            {'name': 'Cryptocurrency', 'description': 'Digital currency investments'},
        ]
        
        for category in asset_categories:
            AssetCategory.objects.get_or_create(
                name=category['name'],
                defaults={'description': category['description']}
            )
        self.stdout.write(self.style.SUCCESS(f'Created {len(asset_categories)} asset categories'))
        
        # Create assets
        stocks_category = AssetCategory.objects.get(name='Stocks')
        etfs_category = AssetCategory.objects.get(name='ETFs')
        bonds_category = AssetCategory.objects.get(name='Bonds')
        real_estate_category = AssetCategory.objects.get(name='Real Estate')
        crypto_category = AssetCategory.objects.get(name='Cryptocurrency')
        
        assets = [
            # Stocks
            {'name': 'AAPL', 'description': 'Apple Inc.', 'current_price': Decimal('180.50'), 'category': stocks_category},
            {'name': 'MSFT', 'description': 'Microsoft Corporation', 'current_price': Decimal('320.75'), 'category': stocks_category},
            {'name': 'GOOGL', 'description': 'Alphabet Inc.', 'current_price': Decimal('140.25'), 'category': stocks_category},
            {'name': 'AMZN', 'description': 'Amazon.com Inc.', 'current_price': Decimal('135.80'), 'category': stocks_category},
            
            # ETFs
            {'name': 'SPY', 'description': 'SPDR S&P 500 ETF Trust', 'current_price': Decimal('420.50'), 'category': etfs_category},
            {'name': 'VTI', 'description': 'Vanguard Total Stock Market ETF', 'current_price': Decimal('215.30'), 'category': etfs_category},
            
            # Bonds
            {'name': 'BND', 'description': 'Vanguard Total Bond Market ETF', 'current_price': Decimal('72.45'), 'category': bonds_category},
            {'name': 'GOVT', 'description': 'iShares U.S. Treasury Bond ETF', 'current_price': Decimal('25.10'), 'category': bonds_category},
            
            # Real Estate
            {'name': 'Rental Property', 'description': '2-bedroom apartment in downtown', 'current_price': Decimal('350000.00'), 'category': real_estate_category},
            {'name': 'VNQ', 'description': 'Vanguard Real Estate ETF', 'current_price': Decimal('84.25'), 'category': real_estate_category},
            
            # Cryptocurrency
            {'name': 'BTC', 'description': 'Bitcoin', 'current_price': Decimal('45000.00'), 'category': crypto_category},
            {'name': 'ETH', 'description': 'Ethereum', 'current_price': Decimal('3200.00'), 'category': crypto_category},
        ]
        
        asset_objects = []
        for asset in assets:
            asset_obj, created = Asset.objects.get_or_create(
                name=asset['name'],
                defaults={
                    'description': asset['description'],
                    'current_price': asset['current_price'],
                    'category': asset['category']
                }
            )
            asset_objects.append(asset_obj)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(assets)} assets'))
        
        # Create transactions (purchases and sales)
        transactions = []
        
        # Start date 6 months ago
        transaction_start_date = timezone.now().date() - timedelta(days=180)
        
        for i in range(180):
            if random.random() < 0.2:  # 20% chance of transaction on a given day
                asset = random.choice(asset_objects)
                transaction_type = random.choice(['buy', 'sell'])
                
                # Quantity based on asset price
                if asset.current_price > 1000:
                    quantity = Decimal(str(round(random.uniform(0.1, 2), 2)))
                elif asset.current_price > 100:
                    quantity = Decimal(str(round(random.uniform(1, 10), 2)))
                else:
                    quantity = Decimal(str(round(random.uniform(1, 50), 2)))
                
                # Price with some variation from current price
                price_variation = random.uniform(0.85, 1.15)
                price = asset.current_price * Decimal(str(price_variation))
                
                current_date = transaction_start_date + timedelta(days=i)
                
                description = f"{transaction_type.capitalize()} {quantity} of {asset.name}"
                
                transactions.append(Transaction(
                    asset=asset,
                    transaction_type=transaction_type,
                    quantity=quantity,
                    price=price,
                    date=current_date,
                    description=description
                ))
        
        # Bulk create transactions
        Transaction.objects.bulk_create(transactions)
        self.stdout.write(self.style.SUCCESS(f'Created {len(transactions)} transactions'))
        
        self.stdout.write(self.style.SUCCESS('Fake data creation completed!'))
