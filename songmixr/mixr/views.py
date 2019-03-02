from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from mixr.models import *
from mixr.forms import HomeForm
from django.db.models import Q
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials



spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'
    def get(self, request):
        form = HomeForm()

        return render(request, self.template_name, args)
