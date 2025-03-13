# Dashboard Cryptocurrency Value Fix Plan

## Issue Identified

The dashboard is showing "Crypto Assets: PLN 0.00" despite having cryptocurrencies in the system. After analyzing the code, I've identified the following issues:

1. The dashboard view calculates the crypto_value using the current_value property of the Cryptocurrency model:
   ```python
   crypto_value = sum(crypto.current_value for crypto in Cryptocurrency.objects.all())
   ```

2. However, unlike the crypto_list view, the dashboard view doesn't update the cryptocurrency prices before calculating the value.

3. The current_value property depends on the current_price field, which may not be updated with the latest prices.

## Solution Plan

### 1. Update the Dashboard View

Modify the dashboard view in core/views.py to update cryptocurrency prices before calculating the total value:

```python
# Portfolio value
cryptocurrencies = Cryptocurrency.objects.all()
try:
    # Update crypto prices before calculating value
    from portfolio.services import CoinGeckoService
    CoinGeckoService.update_crypto_prices(cryptocurrencies)
except Exception as e:
    messages.warning(request, f"Could not update cryptocurrency prices: {str(e)}")

crypto_value = sum(crypto.current_value for crypto in cryptocurrencies)
```

### 2. Ensure Proper Error Handling

Add proper error handling to prevent the dashboard from breaking if the CoinGecko API is unavailable.

### 3. Add Caching (Optional Enhancement)

To improve performance and reduce API calls, consider implementing caching for cryptocurrency prices:

- Cache prices for a reasonable period (e.g., 15 minutes)
- Only make API calls when the cache expires
- This prevents making API calls on every dashboard view

### 4. Add Visual Indicators

Add visual indicators to show when prices were last updated:
- Add a "Last Updated" timestamp on the dashboard
- Add refresh button to manually update prices

## Implementation Steps

1. Switch to Code mode to implement the dashboard view update
2. Test the dashboard to ensure crypto values are displayed correctly
3. Implement optional enhancements if desired

## Technical Considerations

- The CoinGeckoService.update_crypto_prices method already handles API rate limiting and error handling
- The current_value property in the Cryptocurrency model has been fixed to handle Decimal and float type conversion
- Consider the frequency of dashboard views and potential API rate limits