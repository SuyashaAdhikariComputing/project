
from django.urls import path, include
from blog import views

urlpatterns = [
    path('campaignhome/',views.campaignhome, name='campaignhome'),
    path('createcampaign/',views.createcampaign, name='createcampaign'),
    path('<str:slug>/',views.campaignpost, name='campaignpost'),
]