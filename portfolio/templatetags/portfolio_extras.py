
from django import template

register = template.Library()

@register.filter
def format_currency(value):
    """
    Format currency values in a human-readable way.
    Examples: 
        1234 -> PLN 1.2k
        1234567 -> PLN 1.2M
    """
    try:
        value = float(value)
        if value >= 1000000:
            return f"PLN {value/1000000:.1f}M"
        elif value >= 1000:
            return f"PLN {value/1000:.1f}k"
        else:
            return f"PLN {value:.0f}"
    except (ValueError, TypeError):
        return value
