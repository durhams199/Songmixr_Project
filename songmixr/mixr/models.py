from django.db import models
from django.urls import reverse 

# Create your models here.
class Playlist(models.Model):
    playlist_id = models.IntegerField(primary_key=True)
    featured = models.BooleanField(default=False)
    user_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    spotify_playlist_id = models.CharField(max_length=40)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('playlist-detail', args=[str(self.playlist_id)])
