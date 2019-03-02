from django.urls import path, include

from .views import *
#a9011853c8a2404582cedb38966842c4
#989aafd2ae76470ab4a862c48a1b933a
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]