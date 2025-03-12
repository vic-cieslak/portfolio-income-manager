
import random
from datetime import datetime, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from income.models import Income, IncomeCategory

class Command(BaseCommand):
    help = 'Creates fake data for income testing'
    
    def handle(self, *args, **kwargs):
        self.stdout.write('Creating fake income data...')
        
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
                    description=f'Fake {category.name} income generated for testing'
                )
            
            current_date += timedelta(days=1)
        
        total_created = Income.objects.filter(date__gte=start_date, date__lte=end_date).count()
        self.stdout.write(self.style.SUCCESS(f'Successfully created {total_created} fake income entries'))
