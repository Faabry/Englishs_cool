# app_learn_pics/templatetags/array_index.py
from django import template
register = template.Library()

@register.filter
def index(array, i):
    return array[i]