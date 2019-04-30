from django.db import models
from django.urls import reverse 
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in

# Create your models here.
class Playlist(models.Model):
    featured = models.BooleanField(default=False)
    user_id = models.CharField(max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    spotify_playlist_id = models.CharField(max_length=40, primary_key=True)

    def get_absolute_url(self):
        return reverse('playlist-detail', args=[str(self.spotify_playlist_id)])

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.IntegerField(default=0)
    lifetime_likes = models.IntegerField(default=0)
    access_token = models.CharField(max_length=200)

def save_token(sender, user, request, **kwargs):
    print("YES")

user_logged_in.connect(save_token)

