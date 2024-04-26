from django import template

register = template.Library()

@register.filter
def isinstance(value, class_str):
    try:
        return isinstance(value, eval(class_str))
    except (ValueError, TypeError):
        return False