import calendar

from django import template

register = template.Library()


@register.filter
def month_name(value):
    return calendar.month_name[value]
