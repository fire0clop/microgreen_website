from django import template

register = template.Library()

@register.filter
def total_price(items):
    total = 0
    for item in items:
        total += item.get_total_price()
    return total