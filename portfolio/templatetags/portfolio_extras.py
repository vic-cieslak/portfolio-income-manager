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
def percentage(value):
    """Format value as percentage"""
    if value is None:
        return "0%"
    return f"{value:.1f}%"