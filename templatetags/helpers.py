import datetime
from django import template
from django.utils.timezone import localtime

register = template.Library()


@register.filter
def formatted_date(value):
    if not value:
        return ''

    now = localtime(datetime.datetime.now())
    value = localtime(value)

    if value.date() == now.date():
        return value.strftime('%H:%M')
    elif value.date() == (now + datetime.timedelta(days=1)).date():
        return 'Tomorrow'
    else:
        return value.strftime('%Y-%m-%d')
