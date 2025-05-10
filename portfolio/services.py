import requests
import time
from django.utils import timezone
from django.contrib import messages
from decimal import Decimal

class CoinGeckoService:
    """
    Service class for interacting with the CoinGecko API
    """
    BASE_URL = "https://api.coingecko.com/api/v3"

    @classmethod
    def record_portfolio_value(cls):
        """
        Record current portfolio value in the history table
        Only records once per day
        """
        from portfolio.models import Cryptocurrency, BankAccount, PortfolioHistory
        from django.db.models import Sum
        
        # Check if we already have a record for today
        today = timezone.now().date()
        if PortfolioHistory.objects.filter(date=today).exists():
            return False
        
        # Get current values
        cryptocurrencies = Cryptocurrency.objects.all()
        cls.update_crypto_prices(cryptocurrencies)
        
        crypto_value = sum(crypto.current_value for crypto in cryptocurrencies)
        bank_value = BankAccount.objects.aggregate(Sum('balance'))['balance__sum'] or 0
        
        # Create new history record
        PortfolioHistory.objects.create(
            date=today,
            crypto_value=crypto_value,
            bank_value=bank_value
        )
        
        return True
    
    @classmethod
    def _handle_rate_limit(cls, response):
        """
        Handle API rate limiting
        If rate limited, wait and retry
        """
        if response.status_code == 429:  # Too Many Requests
            # Get retry-after header or default to 60 seconds
            retry_after = int(response.headers.get('Retry-After', 60))
            print(f"Rate limited by CoinGecko API. Waiting {retry_after} seconds...")
            time.sleep(retry_after)
            return True
        return False
    
    @classmethod
    def get_top_cryptocurrencies(cls, limit=100):
        """
        Get a list of top cryptocurrencies by market cap
        Returns a list of tuples (id, name) for use in form choices
        """
        try:
            max_retries = 3
            retry_count = 0
            coins = None
            
            while retry_count < max_retries and coins is None:
                response = requests.get(
                    f"{cls.BASE_URL}/coins/markets",
                    params={
                        "vs_currency": "pln",
                        "order": "market_cap_desc",
                        "per_page": limit,
                        "page": 1
                    }
                )
                
                # Handle rate limiting
                if cls._handle_rate_limit(response):
                    retry_count += 1
                    continue
                
                response.raise_for_status()
                coins = response.json()
            
            # Format as choices for Django form
            choices = [(coin["id"], f"{coin['name']} ({coin['symbol'].upper()})") for coin in coins]
            return choices
        except Exception as e:
            print(f"Error fetching top cryptocurrencies: {str(e)}")
            return []
    
    @classmethod
    def get_coin_list(cls):
        """
        Get a list of all coins from CoinGecko API
        Returns a list of dictionaries with id, name, and symbol
        """
        try:
            max_retries = 3
            retry_count = 0
            coin_list = None
            
            while retry_count < max_retries and coin_list is None:
                response = requests.get(f"{cls.BASE_URL}/coins/list")
                
                # Handle rate limiting
                if cls._handle_rate_limit(response):
                    retry_count += 1
                    continue
                
                response.raise_for_status()
                coin_list = response.json()
                return coin_list
        except Exception as e:
            print(f"Error fetching coin list: {str(e)}")
            return []
    
    @classmethod
    def get_coin_data(cls, coin_id):
        """
        Get detailed data for a specific coin
        Returns a dictionary with coin data or None if an error occurs
        """
        try:
            max_retries = 3
            retry_count = 0
            price_data = None
            coin_data = None
            
            # Get current price in PLN
            while retry_count < max_retries and price_data is None:
                price_response = requests.get(
                    f"{cls.BASE_URL}/simple/price",
                    params={
                        "ids": coin_id,
                        "vs_currencies": "pln"
                    }
                )
                
                # Handle rate limiting
                if cls._handle_rate_limit(price_response):
                    retry_count += 1
                    continue
                
                price_response.raise_for_status()
                price_data = price_response.json()
            
            # Reset retry counter
            retry_count = 0
            
            # Get coin details
            while retry_count < max_retries and coin_data is None:
                coin_response = requests.get(f"{cls.BASE_URL}/coins/{coin_id}")
                
                # Handle rate limiting
                if cls._handle_rate_limit(coin_response):
                    retry_count += 1
                    continue
                
                coin_response.raise_for_status()
                coin_data = coin_response.json()
            
            # Combine the data
            return {
                "id": coin_data["id"],
                "name": coin_data["name"],
                "symbol": coin_data["symbol"].upper(),
                "current_price": Decimal(str(price_data[coin_id]["pln"])) if coin_id in price_data else Decimal('0'),
                "image": coin_data["image"]["small"]
            }
        except Exception as e:
            print(f"Error fetching coin data for {coin_id}: {str(e)}")
            return None
    
    @classmethod
    def update_crypto_prices(cls, cryptocurrencies):
        """
        Update cryptocurrency prices from CoinGecko API
        Takes a queryset of Cryptocurrency objects and updates their prices
        """
        if not cryptocurrencies:
            return
        
        # Get all crypto IDs
        crypto_ids = [crypto.coin_id for crypto in cryptocurrencies]
        crypto_ids_str = ",".join(crypto_ids)
        
        try:
            max_retries = 3
            retry_count = 0
            
            while retry_count < max_retries:
                response = requests.get(
                    f"{cls.BASE_URL}/simple/price",
                    params={
                        "ids": crypto_ids_str,
                        "vs_currencies": "pln"
                    }
                )
                
                # Handle rate limiting
                if cls._handle_rate_limit(response):
                    retry_count += 1
                    continue
                
                response.raise_for_status()
                data = response.json()
                break
            
            for crypto in cryptocurrencies:
                if crypto.coin_id in data:
                    crypto.current_price = Decimal(str(data[crypto.coin_id]["pln"]))
                    crypto.last_updated = timezone.now()
                    crypto.save()
        except Exception as e:
            print(f"Error updating crypto prices: {str(e)}")

    @classmethod
    def update_or_create_portfolio_history_for_date(cls, target_date):
        """
        Calculates portfolio value using current crypto prices and bank balances,
        then updates or creates a PortfolioHistory record for the target_date.
        """
        from portfolio.models import Cryptocurrency, BankAccount, PortfolioHistory # Ensure all are imported
        from django.db.models import Sum # Ensure Sum is imported
        
        # Get current crypto values
        cryptocurrencies = Cryptocurrency.objects.all()
        if cryptocurrencies.exists(): # Only update if there are cryptos to track
            cls.update_crypto_prices(cryptocurrencies) # Updates current_price on each crypto instance
        
        crypto_value = sum(crypto.current_value for crypto in cryptocurrencies if crypto.current_value is not None)
        
        # Get current bank values
        bank_value = BankAccount.objects.aggregate(total_balance=Sum('balance'))['total_balance'] or Decimal('0.00')
        
        history_record, created = PortfolioHistory.objects.update_or_create(
            date=target_date,
            defaults={
                'crypto_value': crypto_value,
                'bank_value': bank_value
            }
        )
        return history_record, created
