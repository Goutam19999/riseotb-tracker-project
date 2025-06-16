from django import template

register = template.Library()

@register.filter
def join_labels(value):
    """
    Converts ['Text on Image', 'Spam'] → "Text on Image, Spam"
    """
    if isinstance(value, list):
        return ', '.join(str(v) for v in value)
    return value
