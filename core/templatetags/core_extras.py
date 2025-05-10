from django import template
import math

register = template.Library()

@register.filter(name='humanize_k')
def humanize_k(value):
    try:
        value = float(value)
    except (ValueError, TypeError):
        return value  # Return original value if conversion fails

    if value >= 1000000: # Millions
        return f"{value / 1000000:.1f}M"
    if value >= 1000: # Thousands
        # Check if it's a whole number after division
        if (value / 1000) % 1 == 0:
            return f"{int(value / 1000)}k"
        else:
            return f"{value / 1000:.1f}k"
    return str(value) # Return as string if less than 1000
