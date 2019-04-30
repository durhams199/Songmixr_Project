from django import template
from spotipy import *
from mixr.models import *
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
import json
import spotipy
import spotipy.util as util

register = template.Library()

@register.filter(name='user_photo')
def user_photo(result):
    User_SP = spotipy.Spotify(auth=result.access_token)
    return User_SP.current_user()['images'][0]['url']

@register.filter(name='full_name')
def full_name(result):
    return f'{result.user_id.first_name + " " + result.user_id.last_name}'

@register.filter(name='total_playlists')
def total_playlists(result):
    return Playlist.objects.filter(user_id = result.user_id).count()

@register.filter(name='playlist_list')
def playlist_list(result):
    return Playlist.objects.filter(user_id = result.user_id)

