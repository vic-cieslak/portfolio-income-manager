
from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def currency_format(value):
    """
    Format currency value into a readable format with PLN prefix
    Examples:
    - 1234 becomes "PLN 1.2k"
    - 1234567 becomes "PLN 1.2M"
    - 1234567890 becomes "PLN 1.2B"
    """
    if value is None:
        return "PLN 0"
    
    value = Decimal(value)
    
    if value < 0:
        sign = "-"
        value = abs(value)
    else:
        sign = ""
    
    if value < 1000:
        return f"PLN {sign}{value:.2f}"
    elif value < 1000000:
        return f"PLN {sign}{value/1000:.1f}k"
    elif value < 1000000000:
        return f"PLN {sign}{value/1000000:.1f}M"
    else:
        return f"PLN {sign}{value/1000000000:.1f}B"

@register.filter
def percentage(value):
    """Format value as percentage"""
    if value is None:
        return "0%"
    return f"{value:.1f}%"
