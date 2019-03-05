from django.urls import path, include

from .views import *
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('playlist/<int:pk> ', PlaylistDetailView.as_view(), name='playlist-detail'),
]