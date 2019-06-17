from django.db import models
from django.urls import reverse 
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from social_django.models import UserSocialAuth
from mixr.templatetags import *

# playlist model that represents user playlists
class Playlist(models.Model):
    # used to feature playlists on front page of site
    featured = models.BooleanField(default=False)
    # user associated with the playlist
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # number of likes associated with playlist
    likes = models.IntegerField(default=0)
    # records when playlist was created
    created_at = models.DateTimeField(auto_now_add=True)
    # records when playlist was last updated
    updated_at = models.DateTimeField(auto_now=True)
    # id used to fetch playlist from spotify
    spotify_playlist_id = models.CharField(max_length=40, primary_key=True)

    # used for playlist detail view
    def get_absolute_url(self):
        return reverse('playlist-detail', args=[str(self.spotify_playlist_id)])

# profile model that stores custom user information
class Profile(models.Model):
    # user associated with profile (one to one)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    # records username associated with profile (spotify username)
    prof_username = models.CharField(max_length=30, primary_key=True)
    # records number of followers for a given user
    followers = models.IntegerField(default=0)
    # records total number of likes on all playlists
    lifetime_likes = models.IntegerField(default=0)
    # temporary access token used to retrieve user information (refreshes on login)
    access_token = models.CharField(max_length=200, blank=True, null=True)
    # profile picture for user (spotify photo)
    photo_url = models.CharField(max_length=150, blank=True, null=True)

    # string reperesentation for profile is username
    def __str__(self):
        return f'{self.user_id.username}'

    # used for profile detail view
    def get_absolute_url(self):
        return reverse('profile-detail', args =[str(self.user_id.username)])

# like model that stores a like for a playlist
class Like(models.Model):
    like_from = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_id = models.ForeignKey(Playlist, on_delete=models.CASCADE)


# generates user profile if they don't have one - runs when a user is logged in
def save_token_with_photo(sender, user, request, **kwargs):
    # allows admin to log in without generating profile
    if user.username == 'admin':
        return

    # checks to see if user profile exists already
    # if not, then profile is generated using spotify information    
    if not Profile.objects.filter(user_id = user).exists():
        Profile.objects.create(user_id = user,
                               prof_username = user.username)
    
    # retrieves created/existing profile   
    user_profile = Profile.objects.get(user_id = user)

    # retrieves information for spotify user stored in social_auth metadata
    current_user = request.user.social_auth.filter(provider="spotify")
    
    # retrieves and assigns temporary access token for user
    for user in current_user:
        token = user.extra_data['access_token']
    
    user_profile.access_token = token
    
    # Opens connection to spotify to retrieve photo using token
    User_SP = spotipy.Spotify(auth=token)
    # assigns user photo
    user_profile.photo_url = User_SP.current_user()['images'][0]['url']
    # saves all changes
    user_profile.save()

# calls save_token_with_photo when user is logged in
user_logged_in.connect(save_token_with_photo)

