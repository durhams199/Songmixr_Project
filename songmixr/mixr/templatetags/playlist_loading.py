from django import template
from spotipy import *
from mixr.models import *
from django.conf import settings
from django.db import models
import json
import spotipy
import spotipy.util as util

register = template.Library()

@register.filter(name='playlist_name')
def playlist_name(result):
    playlist = settings.SP.user_playlist(user='', playlist_id= result.spotify_playlist_id)
    return playlist['name']

@register.filter(name='playlist_photo')
def playlist_photo(result):
    playlist = settings.SP.user_playlist(user='', playlist_id= result.spotify_playlist_id)
    return playlist['images'][0]['url']

@register.filter(name='profile_id')
def profile_id(result):
    return str(result.user_id.profile.get_absolute_url())

@register.filter(name='playlist_owner')
def playlist_owner(result):
    playlist = settings.SP.user_playlist(user='', playlist_id= result.spotify_playlist_id)
    user_link = playlist['owner']['external_urls']['spotify']
    return user_link[user_link.find('user/') + 5:]

@register.filter(name='playlist_id')
def playlist_id(result):
    playlist = settings.SP.user_playlist(user='', playlist_id= result.spotify_playlist_id)
    playlist_link = playlist['external_urls']['spotify']
    spotify_playlist_id_temp = playlist_link[playlist_link.find('playlist/') + 9:]
    true_playlist_id = Playlist.objects.filter(spotify_playlist_id = spotify_playlist_id_temp)
    return true_playlist_id[0].get_absolute_url()

@register.filter(name='playlist_tracks')
def playlist_tracks(result):
    playlist = settings.SP.user_playlist(user='', playlist_id= result.spotify_playlist_id, fields = "tracks,next")
    tracks = playlist['tracks']
    track_list = []
    for i, item in enumerate(tracks['items']):
        track = item['track']
        track_list.append(track['name'])  
    return track_list

@register.filter(name='track_artist')
def track_artist(result):
    playlist = settings.SP.user_playlist(user='', playlist_id= result.spotify_playlist_id, fields = "tracks,next")
    tracks = playlist['tracks']
    track_list = []
    for i, item in enumerate(tracks['items']):
        track = item['track']
        artist = item['artist']
        track_list.append(track['name']) 
        artist_list.append(artist['artist']) 

    artists = playlist['artists']
    artist_list = [] 
    for i, item in enumerate(tracks['items']):
        track = item['artist']
        track_list.append(track['name']) 
        artist_list.append(track['artist'])   
    args = {'track_list': track_list, 'artist_list': artist_playlists}
    return args
    
