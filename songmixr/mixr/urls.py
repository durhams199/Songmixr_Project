from django.urls import path, include

from .views import *
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('', include('django.contrib.auth.urls')),
    path('callback/', HomePageView.as_view(), name='home'),
    path('social/', include('social_django.urls')),
    path('accounts/profile/', AccountProfilePageView.as_view(), name='profile'),
    path('accounts/profile/add_playlist', AddPlaylistPageView.as_view(), name='add_playlist'),
    path('playlist/<str:pk>', PlaylistDetailView.as_view(), name='playlist-detail'),
    path('accounts/profile/<str:pk>', ProfileDetailView.as_view(), name='profile-detail'),
    path('login/', HomePageView.as_view(), name='login'),
]