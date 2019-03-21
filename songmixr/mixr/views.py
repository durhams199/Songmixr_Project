from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import TemplateView
from mixr.models import *
from mixr.forms import HomeForm
from django.db import models
import json
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials



# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'
    def get(self, request):
        form = HomeForm()
        featured_playlists = Playlist.objects.filter(featured='True')
        args = {'form': form, 'featured_playlists': featured_playlists}
        return render(request, self.template_name, args)

class LoginPageView(TemplateView):
    template_name = 'login.html'
    def get(self, request):
        form = HomeForm()
        featured_playlists = Playlist.objects.filter(featured='True')
        args = {'form': form, 'featured_playlists': featured_playlists}
        return render(request, self.template_name, args)


from django.views import generic
class PlaylistDetailView(generic.DetailView):
    model = Playlist
