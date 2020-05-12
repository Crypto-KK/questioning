import re
from datetime import datetime, timedelta

from django import template

register = template.Library()


@register.filter
def removeHTML(value):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', value)
    return dd[:300] + '...'

@register.filter
def removeHTML100(value):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', value)
    return dd[:130] + '...'


@register.filter
def processDate(value):
    return value.strftime("%Y-%m-%d")


@register.filter
def process_title(value):
    return value[:20] + '...'


@register.filter
def process_comment_content(value):
    return value[:50] + '...'


@register.filter
def process_time(value):
    value = datetime.strptime(value.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    time_delta = now - value
    if time_delta < timedelta(days=0, hours=1):
        temp = (time_delta.seconds - (time_delta.seconds / 3600) * 3600) / 60
        value = '%s分钟前' % temp
    elif time_delta < timedelta(days=0, hours=24):
        value = '%s小时%s分钟前' % (
        time_delta.seconds // 3600, (time_delta.seconds - (time_delta.seconds / 3600) * 3600) / 60)
    else:
        value = '%s天前' % (time_delta.days)

    return value
