from django import template
from django.template.defaultfilters import floatformat

register = template.Library()

@register.filter
def currency_format(value):
    """Format a number as PLN currency with 2 decimal places"""
    if value is None:
        return "PLN0.00"

    formatted_value = floatformat(value, 2)
    return f"PLN{formatted_value}"

@register.filter
def crypto_price_format(value, currency_symbol="PLN"):
    """Format a number as currency with high precision for crypto prices."""
    if value is None:
        return f"{currency_symbol}0.00"
    
    from decimal import Decimal
    # Determine the number of decimal places needed
    # Show at least 2, but up to 8 for very small numbers
    # This avoids scientific notation from floatformat for very small numbers
    # and ensures we don't show excessive zeros for larger prices.
    val_decimal = Decimal(str(value))
    if val_decimal == Decimal(0):
        num_decimal_places = 2
    else:
        # Calculate how many decimal places to show
        # Aim for about 8 significant digits after the leading zeros
        abs_val = abs(val_decimal)
        if abs_val < Decimal('0.00000001'): # Extremely small, show more
            num_decimal_places = 10
        elif abs_val < Decimal('0.01'): # Small, show up to 8
            num_decimal_places = 8
        elif abs_val < Decimal('1'): # Moderately small, show up to 6
            num_decimal_places = 6
        else: # Larger values, 2 decimal places is fine
            num_decimal_places = 2

    # floatformat with negative arg shows that many decimal places
    formatted_value = floatformat(value, -num_decimal_places) 
    return f"{currency_symbol}{formatted_value}"

@register.filter
def percentage(value):
    """Format value as percentage"""
    if value is None:
        return "0%"
    return f"{value:.1f}%"
