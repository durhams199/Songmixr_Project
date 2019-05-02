from django.db import models
from django.urls import reverse 
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
import json
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from social_django.models import UserSocialAuth
from mixr.templatetags import *

# Create your models here.
class Playlist(models.Model):
    featured = models.BooleanField(default=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    spotify_playlist_id = models.CharField(max_length=40, primary_key=True)

    def get_absolute_url(self):
        return reverse('playlist-detail', args=[str(self.spotify_playlist_id)])

class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    prof_username = models.CharField(max_length=30, primary_key=True)
    followers = models.IntegerField(default=0)
    lifetime_likes = models.IntegerField(default=0)
    access_token = models.CharField(max_length=200, blank=True, null=True)
    photo_url = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f'{self.user_id.username}'

    def get_absolute_url(self):
        return reverse('profile-detail', args =[str(self.user_id.username)])

class Like(models.Model):
    like_from = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_id = models.ForeignKey(Playlist, on_delete=models.CASCADE)

def save_token_with_photo(sender, user, request, **kwargs):
    if user.username == 'admin':
        return
    if not Profile.objects.filter(user_id = user).exists():
        Profile.objects.create(user_id = user,
                               prof_username = user.username)
    user_profile = Profile.objects.get(user_id = user)
    current_user = request.user.social_auth.filter(provider="spotify")
    for user in current_user:
        token = user.extra_data['access_token']
    user_profile.access_token = token
    User_SP = spotipy.Spotify(auth=token)
    user_profile.photo_url = User_SP.current_user()['images'][0]['url']
    user_profile.save()

user_logged_in.connect(save_token_with_photo)

