from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from mixr.models import *
from mixr.forms import HomeForm
from django.db import models
import json
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from social_django.models import UserSocialAuth


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'
    def get(self, request):
        form = HomeForm()
        featured_playlists = Playlist.objects.filter(featured='True')
        '''if request.user.is_authenticated:
            current_username = request.user.username
            current_user = request.user.social_auth.filter(provider="spotify")
            for user in current_user:
                token = user.extra_data['access_token']
            User_SP = spotipy.Spotify(auth=token)
            playlists = User_SP.user_playlists(current_username)
            id_list = []
            for item in playlists['items']:
                temp = item['uri']
                temp = temp[17:]
                id_list.append(temp)
            print(id_list)

            for playlist in id_list[:5]:
                Playlist.objects.create(spotify_playlist_id = playlist,
                                        user_id = current_username,
                                        featured = True)'''


        args = {'form': form, 'featured_playlists': featured_playlists}
        return render(request, self.template_name, args)
class AccountProfilePageView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    def get(self, request):
        form = HomeForm()
        current_username = request.user.username
        current_user = request.user.social_auth.filter(provider="spotify")
        for user in current_user:
            token = user.extra_data['access_token']
        User_SP = spotipy.Spotify(auth=token)
        temp = User_SP.current_user()['images'][0]['url']
        print(temp)

        args = {'form': form}
        return render(request, self.template_name, args)

from django.views import generic
class PlaylistDetailView(generic.DetailView):
    model = Playlist
