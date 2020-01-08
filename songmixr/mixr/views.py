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

# view for home page
class HomePageView(TemplateView):
    template_name = 'home.html'
    login_template = 'registration/login.html'
    
    # Precondition: user has attempted to like/unlike a playlist
    # Postcondition: playlist is liked/unliked, and page is loaded
    def post(self, request):
        args = {}
        # retrieves context for the playlist that was liked/unliked
        liked_playlist_id = request.POST.get('playlist_id')
        playlist = Playlist.objects.get(spotify_playlist_id = liked_playlist_id)
        
        # checks to see if a playlist was liked or unliked
        if request.POST.get("like"):
            
            # checks to see if playlist was liked by authorized user
            if request.user.is_authenticated:
                # checks that playlist isn't already liked from post reauest being refreshed
                if not Like.objects.filter(like_from = request.user,
                                       playlist_id = playlist).exists():
                    
                    # creates like for playlist from user
                    current_user_profile = playlist.user_id.profile
                    Like.objects.create(like_from = request.user,
                                       playlist_id = playlist)
                                        
                    # adds like to user's like count
                    current_user_profile.lifetime_likes += 1
                    current_user_profile.save()
                    
                    # adds like to playlist's like count
                    playlist.likes += 1
                    playlist.save()
                    #User_SP = spotipy.Spotify(auth=request.user.profile.access_token)
                    #User_SP.user_playlist_follow_playlist(playlist.user_id.username, playlist.spotify_playlist_id)
                    #request_user_list = []
                    #request_user_list.append(request.user.username)
                    #print(User_SP.user_playlist_is_following(playlist.user_id.username, playlist.spotify_playlist_id, request_user_list))
            else:
                return render(request, self.login_template, args)

        # checks to see if playlist is being unliked
        if request.POST.get("unlike"):
            # checks if playlist is already liked to avoid repeated action
            if Like.objects.filter(like_from = request.user,
                                   playlist_id = playlist).exists():
                # removes like from database
                current_user_profile = playlist.user_id.profile
                Like.objects.filter(like_from = request.user,
                                   playlist_id = playlist).delete()
                
                # removes a like from user profile                    
                current_user_profile.lifetime_likes -= 1
                current_user_profile.save()

                # remove like from playlist
                playlist.likes -= 1
                playlist.save()
        
        form = HomeForm()

        # resets user for playlist gathering
        current_user_id = None
        if request.user.is_authenticated:
            current_user_id = request.user

        # fetches user's profile
        user_profile = Profile.objects.filter(user_id = current_user_id)
        # fetches features playlists
        featured_playlists = Playlist.objects.filter(featured='True')

        args = {'form': form, 'featured_playlists': featured_playlists, 'user_profile': user_profile}
        return render(request, self.template_name, args)


    def get(self, request):
        form = HomeForm()
        current_user_id = None
        if request.user.is_authenticated:
            current_user_id = request.user

        # user's profile if logged in
        user_profile = Profile.objects.filter(user_id = current_user_id)
        # feteches featured playlists
        featured_playlists = Playlist.objects.filter(featured='True')

        args = {'form': form, 'featured_playlists': featured_playlists, 'user_profile': user_profile}
        return render(request, self.template_name, args)

# generic view for profiles
class AccountProfilePageView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    delete_template_name = 'delete_playlist.html'
    edit_template_name = 'edit_playlist.html'
    login_url = '/login/'

    # occurs when a playlists is edited/deleted
    def post(self, request):

        # gets context for playlist that is to be edited/deleted
        playlist_id = request.POST.get('playlist_id')
        playlist = Playlist.objects.filter(spotify_playlist_id = playlist_id)
        user_profile = Profile.objects.get(user_id = request.user)

        # checks if request was for an edit
        if request.POST.get("edit"):
            template = self.edit_template_name

        # checks if request was for a delete
        if request.POST.get("delete"):
            print("delete")
            template = self.delete_template_name
                
        # checks to see if request was to confirm edit/delete
        if request.POST.get("confirm"):
            # checks if playlist is already deleted (from refreshing page)
            if playlist.exists():
                # deletes playlist, removes likes gained from playlist
                deleted_playlist = Playlist.objects.get(spotify_playlist_id = playlist_id)
                user_profile.lifetime_likes -= deleted_playlist.likes
                user_profile.save()
                Playlist.objects.filter(spotify_playlist_id = playlist_id).delete()

            template = self.template_name

        # checks to see if request was to cancel action
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

class BrowsePageView(TemplateView):
    template_name = 'browse.html'

    def get (self, request):
        form = HomeForm()
        top_users = Profile.objects.all().aggregate(Max(lifetime_likes))[5:]
        args = {'form': form, top_users: 'top_users'}
        return render(request, self.template_name, args)

# page that user is directed to if they attempt to add a new playlist
class AddPlaylistPageView(LoginRequiredMixin, TemplateView):
    template_name = 'add_playlist.html'
    login_url = '/login/'
    
    # occurs when a playlist is selected to be added
    def post(self, request):
        # gets id for added playlist
        playlist_id = request.POST.get('playlist_id')
        # checks to see if page was refreshed to playlist isn't added twice
        if not Playlist.objects.filter(spotify_playlist_id = playlist_id).exists():
            Playlist.objects.create(spotify_playlist_id = playlist_id,
                                    user_id = request.user)
        # gets model for new playlist for confirmation message
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

# login page for when a non authorized user attempts to take authorized action
class LoginPageView(TemplateView):
    template_name = 'login.html'
    def get(self, request):
        form = HomeForm()
        args = {'form': form}
        return render(request, self.template_name, args)


from django.views import generic
# generic playlist view
class PlaylistDetailView(generic.DetailView):
    model = Playlist

    def post(self, request):
        return(request, 'playlist_detail.html')

# generic profile view
class ProfileDetailView(generic.DetailView):
    model = Profile
