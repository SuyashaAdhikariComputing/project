
from django.urls import path, include
from . views import CampaignView,CampaignDetailView, CampaignPostView,CampaignEditView
from campaign import views
urlpatterns = [
    path('campaignhome/',CampaignView.as_view(),name="campaignhome"),
    path('createcampaign/',CampaignPostView.as_view(), name='postcampaign'),
    path('<slug:slug>/', CampaignDetailView.as_view(), name='campaigndetail'),
    path('editcampaign/<slug:slug>/', CampaignEditView.as_view(), name='campaignedit'),
    path('deletecampaign/<slug:slug>/', views.deletecampaign, name='campaigndelete'),
]