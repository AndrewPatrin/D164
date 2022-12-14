from datetime import datetime
from django import template

register = template.Library()


@register.simple_tag()
def current_time(format_string='%d %b %Y - %H:%M:%S'):
    return datetime.now().astimezone().strftime(format_string)


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
