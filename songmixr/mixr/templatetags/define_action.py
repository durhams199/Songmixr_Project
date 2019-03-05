from django import template
from spotipy import *

register = template.Library()

@register.simple_tag
def define(val=None):
    return val
