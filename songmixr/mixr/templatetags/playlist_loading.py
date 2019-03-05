from django import template
from spotipy import *
from mixr.models import *

register = template.Library()

@register.filter(name='playlist_name')
def playlist_name(playlist):
    return playlist['name']

@register.filter(name='playlist_photo')
def playlist_photo(playlist):
    return playlist['images'][0]['url']

@register.filter(name='playlist_owner')
def playlist_owner(playlist):
    user_link = playlist['owner']['external_urls']['spotify']
    return user_link[user_link.find('user/') + 5:]

@register.filter(name='playlist_id')
def playlist_id(playlist):
    playlist_link = playlist['external_urls']['spotify']
    spotify_playlist_id_temp = playlist_link[playlist_link.find('playlist/') + 9:]
    true_playlist_id = Playlist.objects.filter(spotify_playlist_id = spotify_playlist_id_temp)
    return true_playlist_id[0].get_absolute_url()

@register.filter(name='spotify_playlist_id')
def spotify_playlist_id(playlist):
    playlist_link = playlist['external_urls']['spotify']
    return playlist_link[playlist_link.find('/playlist/') + 9:]