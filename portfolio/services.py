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