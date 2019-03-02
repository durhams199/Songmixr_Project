from django.db import models

# Create your models here.
class Playlist(models.Model):
    playlist_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    spotify_playlist_id = models.CharField(max_length=20)
