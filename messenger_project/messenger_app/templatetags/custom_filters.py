from django import template

register = template.Library()


@register.filter(name='get_month_and_day')
def get_month_and_day(value):
    if value:
        return f'{value[5:7]}.{value[8:10]} {value[11:16]}'
    return ''