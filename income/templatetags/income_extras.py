from django import template
import calendar

register = template.Library()

@register.filter
def split(value, delimiter):
    """
    Returns the string split by delimiter.
    """
    return value.split(delimiter)

@register.filter
def get_item(dictionary, key):
    """
    Gets an item from a dictionary using the key.
    """
    return dictionary.get(key)

@register.filter
def month_days(year, month):
    """Return a list of weeks, each containing 7 days (0 for days outside the month)"""
    cal = calendar.monthcalendar(year, month)
    return cal