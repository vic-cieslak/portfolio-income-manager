
from django import template
import calendar

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Gets an item from a dictionary using the key.
    """
    if dictionary is None:
        return None
    return dictionary.get(key)

@register.filter
def month_days(year, month):
    """Return a list of weeks, each containing 7 days (0 for days outside the month)"""
    cal = calendar.monthcalendar(year, month)
    return cal

@register.filter
def format_currency(value):
    """
    Format currency values to show 'k' suffix for thousands.
    Example: 1300 -> 1.3k, 500 -> 500.00
    """
    try:
        value = float(value)
        if value >= 1000:
            return f"{value/1000:.1f}k"
        else:
            return f"{value:.2f}"
    except (ValueError, TypeError):
        return value
