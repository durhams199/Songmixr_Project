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
from mixr.templatetags import *


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'
    login_url = '/login/'
    
    def post(self, request):
        args = {}
        liked_playlist_id = request.POST.get('playlist_id')
        playlist = Playlist.objects.get(spotify_playlist_id = liked_playlist_id)
        
        if request.POST.get("like"):
            
            if request.user.is_authenticated:
                if not Like.objects.filter(like_from = request.user,
                                       playlist_id = playlist).exists():
                    current_user_profile = playlist.user_id.profile
                    Like.objects.create(like_from = request.user,
                                       playlist_id = playlist)
                                        
                    current_user_profile.lifetime_likes += 1
                    current_user_profile.save()
                    playlist.likes += 1
                    playlist.save()
                    #User_SP = spotipy.Spotify(auth=request.user.profile.access_token)
                    #User_SP.user_playlist_follow_playlist(playlist.user_id.username, playlist.spotify_playlist_id)
                    #request_user_list = []
                    #request_user_list.append(request.user.username)
                    #print(User_SP.user_playlist_is_following(playlist.user_id.username, playlist.spotify_playlist_id, request_user_list))
            else:
                return render(request, self.login_url, args)


        if request.POST.get("unlike"):
            if Like.objects.filter(like_from = request.user,
                                   playlist_id = playlist).exists():
                current_user_profile = playlist.user_id.profile
                Like.objects.filter(like_from = request.user,
                                   playlist_id = playlist).delete()
                                    
                current_user_profile.lifetime_likes -= 1
                current_user_profile.save()
                playlist.likes -= 1
                playlist.save()
        
        form = HomeForm()

        current_user_id = None
        if request.user.is_authenticated:
            current_user_id = request.user

        user_profile = Profile.objects.filter(user_id = current_user_id)
        featured_playlists = Playlist.objects.filter(featured='True')

        args = {'form': form, 'featured_playlists': featured_playlists, 'user_profile': user_profile}
        return render(request, self.template_name, args)

    def get(self, request):
        form = HomeForm()
        current_user_id = None
        if request.user.is_authenticated:
            current_user_id = request.user

        user_profile = Profile.objects.filter(user_id = current_user_id)
        featured_playlists = Playlist.objects.filter(featured='True')

        args = {'form': form, 'featured_playlists': featured_playlists, 'user_profile': user_profile}
        return render(request, self.template_name, args)

class AccountProfilePageView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    delete_template_name = 'delete_playlist.html'
    edit_template_name = 'edit_playlist.html'
    login_url = '/login/'

    def post(self, request):
        playlist_id = request.POST.get('playlist_id')
        print("playlist id:")
        print(playlist_id)
        playlist = Playlist.objects.filter(spotify_playlist_id = playlist_id)
        user_profile = Profile.objects.get(user_id = request.user)

        if request.POST.get("edit"):
            print("edit")
            template = self.edit_template_name

        if request.POST.get("delete"):
            print("delete")
            template = self.delete_template_name
                

        if request.POST.get("confirm"):
            print("confirm")
            print(request.POST.get('playlist_id'))
            if playlist.exists():
                print("IT DID")
                deleted_playlist = Playlist.objects.get(spotify_playlist_id = playlist_id)
                user_profile.lifetime_likes -= deleted_playlist.likes
                user_profile.save()
                Playlist.objects.filter(spotify_playlist_id = playlist_id).delete()

            template = self.template_name

        if request.POST.get("cancel"):
            print("cancel")
            template = self.template_name
        
        form = HomeForm()
        args = {'form': form, 'user_profile': user_profile, 'playlist': playlist}
        return render(request, template, args)

    def get(self, request):
        form = HomeForm()
        user_profile = Profile.objects.get(user_id = request.user)
        args = {'form': form, 'user_profile': user_profile}
        return render(request, self.template_name, args)

class AddPlaylistPageView(LoginRequiredMixin, TemplateView):
    template_name = 'add_playlist.html'
    login_url = '/login/'
    
    def post(self, request):
        playlist_id = request.POST.get('playlist_id')
        if not Playlist.objects.filter(spotify_playlist_id = playlist_id).exists():
            Playlist.objects.create(spotify_playlist_id = playlist_id,
                                    user_id = request.user)
        playlist = Playlist.objects.filter(spotify_playlist_id = playlist_id)
        
        form = HomeForm()
        user_profile = Profile.objects.get(user_id = request.user)
        args = {'form': form, 'user_profile': user_profile, 'playlist': playlist}
        return render(request, self.template_name, args)

    def get(self, request):
        form = HomeForm()
        user_profile = Profile.objects.get(user_id = request.user)
        args = {'form': form, 'user_profile': user_profile}
        return render(request, self.template_name, args)

class LoginPageView(TemplateView):
    template_name = 'login.html'
    def get(self, request):
        form = HomeForm()
        args = {'form': form}
        return render(request, self.template_name, args)


from django.views import generic
class PlaylistDetailView(generic.DetailView):
    model = Playlist

    def post(self, request):
        return(request, 'playlist_detail.html')

class ProfileDetailView(generic.DetailView):
    model = Profile
