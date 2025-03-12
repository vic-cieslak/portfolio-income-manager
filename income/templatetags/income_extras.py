from django import template
import calendar
from datetime import datetime, date

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def month_days(year, month):
    """Return a list of weeks, each containing 7 days (0 for days outside the month)"""
    cal = calendar.monthcalendar(year, month)
    return cal

@register.filter
def split(value, delimiter=' '):
    """Split a string into a list by delimiter"""
    return value.split(delimiter)

# You can add more custom template filters or tags here

from django.shortcuts import render

def income_calendar(request, year=None, month=None):
    now = datetime.now()
    year = int(year) if year else now.year
    month = int(month) if month else now.month

    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]

    context = {
        'month_days': cal,
        'month_name': month_name,
        'year': year,
    }
    return render(request, 'income/income_calendar.html', context)

#income/income_calendar.html

<h1>Income Calendar - {{ year }} {{ month_name }}</h1>

<table>
  <thead>
    <tr>
      {% for day in "Mon Tue Wed Thu Fri Sat Sun"|split:" " %}
        <th>{{ day }}</th>
      {% endfor %}
    </tr>
  </thead>
  <tbody>
    {% for week in month_days %}
      <tr>
        {% for day in week %}
          <td>{% if day > 0 %}{{ day }}{% endif %}</td>
        {% endfor %}
      </tr>
    {% endfor %}
  </tbody>
</table>