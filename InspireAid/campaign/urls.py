
from django.urls import path, include
from . views import CampaignView,CampaignDetailView

urlpatterns = [
    path('campaignhome/',CampaignView.as_view(),name="campaignhome"),
    path('<slug:slug>/', CampaignDetailView.as_view(), name='campaigndetail'),
]