from django import template

register = template.Library()

@register.filter
def split(value, delimiter=':'):
    """Stringni bo'lib list qaytaradi"""
    return value.split(delimiter)