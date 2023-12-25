import math

from django import template

register = template.Library()

@register.filter
def div(a, b):
    if b != 0:
        return a / b
    return 0

@register.filter
def mul(a, b):
    return a * b

@register.filter
def trunc(a):
    return math.trunc(a)