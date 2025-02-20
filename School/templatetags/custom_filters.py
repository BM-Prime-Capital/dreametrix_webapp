# custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(value, arg):
    return value.get(arg, 0)

register.filter('get_item', get_item)