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

@register.filter(name='spotify_playlist_names')
def spotify_playlist_names(result):
    token = result.access_token
    User_SP = spotipy.Spotify(auth=token)
    playlists = User_SP.user_playlists(result.user_id.username)
    name_list = []
    for item in playlists['items']:
        if item['owner']['id'] == result.user_id.username:
            temp = item['uri']
            temp = temp[17:]
            if not Playlist.objects.filter(spotify_playlist_id = temp).exists():
                name_list.append(item['name'])
    
    return name_list

@register.filter(name='spotify_playlist_id')
def spotify_playlist_id(result):
    token = result.access_token
    User_SP = spotipy.Spotify(auth=token)
    playlists = User_SP.user_playlists(result.user_id.username)
    id_list = []
    for item in playlists['items']:
        if item['owner']['id'] == result.user_id.username:
            temp = item['uri']
            temp = temp[17:]
            if not Playlist.objects.filter(spotify_playlist_id = temp).exists():
                id_list.append(temp)
    return id_list

@register.filter(name='spotify_playlist_track_total')
def spotify_playlist_track_total(result):
    token = result.access_token
    User_SP = spotipy.Spotify(auth=token)
    playlists = User_SP.user_playlists(result.user_id.username)
    track_counts = []
    for item in playlists['items']:
        if item['owner']['id'] == result.user_id.username:
            temp = item['uri']
            temp = temp[17:]
            if not Playlist.objects.filter(spotify_playlist_id = temp).exists():
                track_counts.append(item['tracks']['total'])
    return track_counts

@register.filter(name='liked_playlists')
def liked_playlists(result):
    return Like.objects.filter(like_from = result.first().user_id)
