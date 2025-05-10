import random
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

from income.models import Income, IncomeCategory
from expenses.models import Expense, ExpenseCategory
from portfolio.models import Cryptocurrency, BankAccount, PortfolioHistory

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates realistic fake data for the past 12 months for income, expenses, portfolio, and portfolio history.'

    def get_admin_user(self):
        """Get or create the admin user and return it"""
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Superuser "admin" created successfully.'))
        else:
            admin_user = User.objects.get(username='admin')
            self.stdout.write(self.style.WARNING('Superuser "admin" already exists.'))
        return admin_user

    def create_fake_bank_accounts(self, target_total_balance=Decimal('50000')):
        self.stdout.write(self.style.HTTP_INFO('Creating fake bank accounts...'))
        BankAccount.objects.all().delete() # Clear existing before creating new
        bank_names = ['Millennium Current', 'PKO Savings', 'Revolut PLN', 'Santander Investment']
        num_accounts = random.randint(2, 4)
        created_accounts = []

        # Ensure bank_names is long enough or repeat names if necessary
        selected_bank_names = random.sample(bank_names * (num_accounts // len(bank_names) +1) , num_accounts)


        # Distribute target balance somewhat unevenly
        balances = []
        remaining_balance = target_total_balance
        for i in range(num_accounts - 1):
            # Ensure each account gets a reasonable minimum, and not more than remaining
            max_share = remaining_balance - (num_accounts - 1 - i) * Decimal('1000') # Min 1k for others
            min_share = Decimal('1000')
            if max_share < min_share: max_share = min_share # handle edge case if remaining_balance is too low

            share = Decimal(str(random.uniform(float(min_share), float(max_share))))
            share = min(share, remaining_balance - (num_accounts - 1 - i) * Decimal('1000')) # Don't take too much
            share = share.quantize(Decimal('0.01'))
            balances.append(share)
            remaining_balance -= share
        balances.append(remaining_balance.quantize(Decimal('0.01'))) # Last account gets the rest
        random.shuffle(balances) # Shuffle to make it less predictable

        for i in range(num_accounts):
            name = selected_bank_names[i]
            balance = balances[i]
            if balance < Decimal('0'): # Safety check
                balance = Decimal('1000') # Give a minimum if calculation went wrong

            account = BankAccount.objects.create(
                name=name,
                balance=balance,
                description=f'Fake {name} generated for testing'
            )
            created_accounts.append(account)
            self.stdout.write(f'  Created Bank Account: {name} with balance {balance:.2f} PLN')
        
        actual_total_balance = sum(acc.balance for acc in created_accounts)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(created_accounts)} bank accounts with a total balance of {actual_total_balance:.2f} PLN.'))
        return created_accounts

    def create_fake_cryptocurrencies(self, target_total_value=Decimal('50000')):
        self.stdout.write(self.style.HTTP_INFO('Creating fake cryptocurrencies...'))
        Cryptocurrency.objects.all().delete() # Clear existing
        
        # More diverse and common crypto data
        crypto_data_options = [
            ('bitcoin', 'Bitcoin', 'BTC', Decimal('20000'), Decimal('70000')),  # Min/Max realistic price
            ('ethereum', 'Ethereum', 'ETH', Decimal('1000'), Decimal('4000')),
            ('cardano', 'Cardano', 'ADA', Decimal('0.2'), Decimal('3.0')),
            ('solana', 'Solana', 'SOL', Decimal('10'), Decimal('250')),
            ('polkadot', 'Polkadot', 'DOT', Decimal('3'), Decimal('50')),
            ('dogecoin', 'Dogecoin', 'DOGE', Decimal('0.05'), Decimal('0.7')),
            ('shiba-inu', 'Shiba Inu', 'SHIB', Decimal('0.000007'), Decimal('0.00008'))
        ]
        
        num_cryptos = random.randint(3, 5)
        selected_cryptos_data = random.sample(crypto_data_options, num_cryptos)
        created_cryptos = []

        # Distribute target value
        values_for_each_crypto = []
        remaining_value = target_total_value
        for i in range(num_cryptos - 1):
            max_share = remaining_value - (num_cryptos - 1 - i) * Decimal('1000') # Min 1k value for others
            min_share = Decimal('1000')
            if max_share < min_share: max_share = min_share

            share = Decimal(str(random.uniform(float(min_share), float(max_share))))
            share = min(share, remaining_value - (num_cryptos - 1 - i) * Decimal('1000'))
            share = share.quantize(Decimal('0.01'))
            values_for_each_crypto.append(share)
            remaining_value -= share
        values_for_each_crypto.append(remaining_value.quantize(Decimal('0.01')))
        random.shuffle(values_for_each_crypto)

        for i in range(num_cryptos):
            coin_id, name, symbol, min_price, max_price = selected_cryptos_data[i]
            target_value_for_this_crypto = values_for_each_crypto[i]
            if target_value_for_this_crypto < Decimal('100'): # Ensure a minimum sensible value
                target_value_for_this_crypto = Decimal('100')

            current_price = Decimal(str(random.uniform(float(min_price), float(max_price)))).quantize(Decimal('0.00000001')) # High precision for price
            if current_price == Decimal('0'): # Avoid division by zero
                current_price = min_price if min_price > Decimal('0') else Decimal('0.000001')

            quantity = (target_value_for_this_crypto / current_price).quantize(Decimal('0.00000001')) # 8 decimal places for quantity
            
            acquisition_cost = current_price * quantity # Or could be a different historical price

            crypto = Cryptocurrency.objects.create(
                coin_id=coin_id,
                name=name,
                symbol=symbol,
                quantity=quantity,
                current_price=current_price,
                acquisition_cost=acquisition_cost.quantize(Decimal('0.01'))
            )
            created_cryptos.append(crypto)
            self.stdout.write(f'  Created Crypto: {name} ({symbol}), Quantity: {quantity}, Price: {current_price:.2f} PLN, Value: {(quantity*current_price):.2f} PLN')

        actual_total_value = sum(c.quantity * c.current_price for c in created_cryptos)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(created_cryptos)} cryptocurrencies with a total initial value of {actual_total_value:.2f} PLN.'))
        return created_cryptos

    def create_portfolio_history(self, start_date, end_date, initial_bank_value, initial_crypto_value):
        self.stdout.write(self.style.HTTP_INFO('Creating portfolio history...'))
        PortfolioHistory.objects.all().delete()

        current_bank_value = initial_bank_value
        current_crypto_value = initial_crypto_value
        
        num_days = (end_date - start_date).days + 1
        
        for i in range(num_days):
            current_date = start_date + timedelta(days=i)
            
            if i > 0: # Fluctuate values after the first day
                # Crypto: more volatile
                crypto_change_percent = Decimal(str(random.uniform(-0.05, 0.05))) # -5% to +5%
                current_crypto_value *= (Decimal('1') + crypto_change_percent)
                current_crypto_value = max(Decimal('0'), current_crypto_value) # Ensure not negative

                # Bank: less volatile, generally slight positive or small negative
                bank_change_percent = Decimal(str(random.uniform(-0.005, 0.01))) # -0.5% to +1%
                current_bank_value *= (Decimal('1') + bank_change_percent)
                current_bank_value = max(Decimal('0'), current_bank_value)

            PortfolioHistory.objects.create(
                date=current_date,
                bank_value=current_bank_value.quantize(Decimal('0.01')),
                crypto_value=current_crypto_value.quantize(Decimal('0.01'))
            )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_days} portfolio history entries from {start_date} to {end_date}.'))
        self.stdout.write(f'  Final portfolio history values: Bank={current_bank_value:.2f} PLN, Crypto={current_crypto_value:.2f} PLN')
        return current_bank_value, current_crypto_value


    def update_asset_current_values(self, final_bank_value, final_crypto_value):
        self.stdout.write(self.style.HTTP_INFO('Updating current asset values based on final portfolio history...'))

        # Update Bank Accounts
        bank_accounts = BankAccount.objects.all()
        if bank_accounts:
            # Distribute the final_bank_value proportionally to initial balances
            initial_total_bank = sum(acc.balance for acc in bank_accounts) # This is the balance set during creation
            if initial_total_bank > 0:
                for acc in bank_accounts:
                    proportion = acc.balance / initial_total_bank
                    acc.balance = (final_bank_value * proportion).quantize(Decimal('0.01'))
                    acc.save()
            elif len(bank_accounts) > 0: # If initial total was 0, distribute equally
                equal_share = (final_bank_value / len(bank_accounts)).quantize(Decimal('0.01'))
                for acc in bank_accounts:
                    acc.balance = equal_share
                    acc.save()
            self.stdout.write(self.style.SUCCESS(f'Updated bank account balances. New total: {final_bank_value:.2f} PLN.'))


        # Update Cryptocurrencies
        cryptos = Cryptocurrency.objects.all()
        if cryptos:
            # We want sum(quantity * new_price) = final_crypto_value
            # Keep quantities, adjust prices proportionally to their initial contribution to value
            initial_total_crypto_value_from_creation = sum(c.quantity * c.current_price for c in cryptos)

            if initial_total_crypto_value_from_creation > 0:
                for crypto in cryptos:
                    initial_value_contribution = crypto.quantity * crypto.current_price
                    proportion_of_value = initial_value_contribution / initial_total_crypto_value_from_creation
                    
                    target_value_for_this_crypto = final_crypto_value * proportion_of_value
                    if crypto.quantity > 0:
                        crypto.current_price = (target_value_for_this_crypto / crypto.quantity).quantize(Decimal('0.00000001'))
                    else: # if quantity is 0 for some reason, set price to 0
                        crypto.current_price = Decimal('0')
                    crypto.save()
            elif len(cryptos) > 0: # If initial total value was 0, try to set prices to distribute value
                 # This case is tricky if quantities are also zero or very different.
                 # For simplicity, if initial value was zero, we might just set one crypto to hold the value or distribute prices somewhat arbitrarily.
                 # A better approach might be to re-evaluate quantities if this happens.
                 # For now, let's just assign an arbitrary price based on equal value distribution.
                equal_value_share = final_crypto_value / len(cryptos)
                for crypto in cryptos:
                    if crypto.quantity > 0:
                        crypto.current_price = (equal_value_share / crypto.quantity).quantize(Decimal('0.00000001'))
                    else: # if quantity is 0, can't set a meaningful price to achieve value
                        crypto.current_price = Decimal('0') # Or some small default if quantity is also 0
                    crypto.save()

            new_total_crypto_value = sum(c.quantity * c.current_price for c in cryptos)
            self.stdout.write(self.style.SUCCESS(f'Updated cryptocurrency prices. New total value: {new_total_crypto_value:.2f} PLN.'))


    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.HTTP_INFO('Starting fake data creation process...'))

        # 0. Clear old data
        self.stdout.write(self.style.WARNING('Deleting old data...'))
        Income.objects.all().delete()
        Expense.objects.all().delete()
        # BankAccount and Cryptocurrency are deleted in their respective creation methods
        # PortfolioHistory is deleted in its creation method
        # Categories are handled by get_or_create

        # 1. Get or create admin user
        admin_user = self.get_admin_user()

        # 2. Create income categories
        income_categories_data = [
            ('Salary', 'Regular monthly salary'),
            ('Freelance', 'Income from freelance projects'),
            ('Investments', 'Dividends, interest, capital gains'),
            ('Rental Income', 'Income from rental properties'),
            ('Side Business', 'Income from a side business'),
            ('Gifts', 'Monetary gifts received'),
            ('Other Income', 'Miscellaneous other income')
        ]
        all_income_categories = []
        for name, desc in income_categories_data:
            cat, created = IncomeCategory.objects.get_or_create(name=name, defaults={'description': desc})
            all_income_categories.append(cat)
            if created: self.stdout.write(f'  Created Income Category: {name}')

        # 3. Create expense categories
        expense_categories_data = [
            ('Groceries', 'Food and household supplies'),
            ('Rent/Mortgage', 'Monthly housing payment'),
            ('Utilities', 'Electricity, water, gas, internet'),
            ('Transportation', 'Public transport, fuel, car maintenance'),
            ('Dining Out', 'Restaurants, cafes, takeaways'),
            ('Entertainment', 'Movies, concerts, hobbies'),
            ('Healthcare', 'Medication, doctor visits, insurance'),
            ('Shopping', 'Clothing, electronics, personal items'),
            ('Education', 'Courses, books, tuition fees'),
            ('Travel', 'Vacations, trips'),
            ('Other Expenses', 'Miscellaneous other expenses')
        ]
        all_expense_categories = []
        for name, desc in expense_categories_data:
            cat, created = ExpenseCategory.objects.get_or_create(name=name, defaults={'description': desc})
            all_expense_categories.append(cat)
            if created: self.stdout.write(f'  Created Expense Category: {name}')

        # 4. Create initial Bank Accounts and Cryptocurrencies
        # These will set the *initial* state for portfolio history
        initial_bank_accounts = self.create_fake_bank_accounts(target_total_balance=Decimal('50000'))
        initial_cryptos = self.create_fake_cryptocurrencies(target_total_value=Decimal('50000'))
        
        initial_total_bank_balance = sum(acc.balance for acc in initial_bank_accounts)
        initial_total_crypto_value = sum(c.quantity * c.current_price for c in initial_cryptos)

        # 5. Define date range for 12 months (365 days)
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=364) # 365 days total including end_date

        # 6. Generate Income and Expense entries for the period
        self.stdout.write(self.style.HTTP_INFO(f'Generating income and expenses from {start_date} to {end_date}...'))
        current_date = start_date
        total_income_entries = 0
        total_expense_entries = 0

        while current_date <= end_date:
            # Daily income target: 1000 - 2000 PLN
            daily_income_target = Decimal(str(random.uniform(1000, 2000)))
            current_daily_income = Decimal('0')
            
            # Generate 1-2 primary income entries (e.g., Salary, Freelance)
            num_primary_incomes = random.randint(1, 2)
            for _ in range(num_primary_incomes):
                if current_daily_income >= daily_income_target: break
                
                category_name = random.choice(['Salary', 'Freelance', 'Side Business'])
                category = IncomeCategory.objects.get(name=category_name)
                
                # Calculate amount to reach target, with some randomness
                remaining_target = daily_income_target - current_daily_income
                max_amount = remaining_target / (num_primary_incomes - _ ) # Distribute remaining target
                
                amount = Decimal(str(random.uniform(float(max_amount * Decimal('0.7')), float(max_amount))))
                amount = min(amount, remaining_target) # Don't overshoot
                amount = max(Decimal('50'), amount.quantize(Decimal('0.01'))) # Min amount

                if category.name == 'Salary' and current_date.day == 1: # Monthly salary
                    amount = Decimal(str(random.uniform(4000, 8000))).quantize(Decimal('0.01')) # Larger one-time
                elif category.name == 'Salary': # Skip salary on other days if it's monthly
                    continue


                Income.objects.create(
                    category=category,
                    amount=amount,
                    date=current_date,
                    description=f'Fake {category.name} income',
                    user=admin_user
                )
                current_daily_income += amount
                total_income_entries += 1

            # Optional: Small other incomes
            if random.random() < 0.3: # 30% chance of small other income
                other_cat_names = ['Investments', 'Gifts', 'Other Income']
                category = IncomeCategory.objects.get(name=random.choice(other_cat_names))
                amount = Decimal(str(random.uniform(20, 200))).quantize(Decimal('0.01'))
                Income.objects.create(
                    category=category, amount=amount, date=current_date,
                    description=f'Fake {category.name} income', user=admin_user
                )
                total_income_entries += 1
            
            # Generate 2-5 expense entries per day
            num_expense_entries = random.randint(2, 5)
            for _ in range(num_expense_entries):
                category = random.choice(all_expense_categories)
                
                # More realistic expense amounts based on category
                if category.name in ['Rent/Mortgage'] and current_date.day == 5: # Monthly rent/mortgage
                    amount = Decimal(str(random.uniform(1500, 3500)))
                elif category.name in ['Rent/Mortgage']: # Skip on other days
                    continue
                elif category.name == 'Groceries': amount = Decimal(str(random.uniform(30, 150)))
                elif category.name == 'Utilities': amount = Decimal(str(random.uniform(10, 80))) # More frequent, smaller
                elif category.name == 'Dining Out': amount = Decimal(str(random.uniform(20, 200)))
                elif category.name == 'Transportation': amount = Decimal(str(random.uniform(10, 100)))
                elif category.name == 'Shopping': amount = Decimal(str(random.uniform(50, 500))) # Less frequent, larger
                elif category.name == 'Entertainment': amount = Decimal(str(random.uniform(20, 250)))
                else: amount = Decimal(str(random.uniform(10, 100))) # Default for others
                
                Expense.objects.create(
                    category=category,
                    amount=amount.quantize(Decimal('0.01')),
                    date=current_date,
                    description=f'Fake {category.name} expense',
                    user=admin_user
                )
                total_expense_entries += 1
            
            current_date += timedelta(days=1)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {total_income_entries} income entries.'))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {total_expense_entries} expense entries.'))

        # 7. Create Portfolio History
        final_bank_val, final_crypto_val = self.create_portfolio_history(
            start_date, end_date,
            initial_total_bank_balance, initial_total_crypto_value
        )

        # 8. Update current BankAccount balances and Cryptocurrency prices
        self.update_asset_current_values(final_bank_val, final_crypto_val)

        self.stdout.write(self.style.SUCCESS('Fake data creation process completed successfully!'))
        self.stdout.write(self.style.WARNING('Remember to run `python manage.py backfill_portfolio_history` if you want to use the separate history backfill for any reason, though this script now handles history.'))
        self.stdout.write(self.style.WARNING('The `backfill_portfolio_history` command might have different logic for value fluctuation and might overwrite history generated by this command if run afterwards.'))
