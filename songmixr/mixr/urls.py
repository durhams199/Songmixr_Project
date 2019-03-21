from django.urls import path, include

from .views import *
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('playlist/<str:pk> ', PlaylistDetailView.as_view(), name='playlist-detail'),
]