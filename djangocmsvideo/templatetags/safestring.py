from django.utils.safestring import mark_safe
from django.template import Library

register = Library()
@register.filter(name='safeVideo')
def safeVideo(value):

    for video in value:
        video['caption'] = mark_safe(video['caption'])

    return value
