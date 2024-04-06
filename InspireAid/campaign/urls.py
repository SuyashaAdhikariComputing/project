
from django.urls import path, include
from . views import CampaignView,CampaignDetailView, CampaignPostView,CampaignEditView,DonateFormView
from campaign import views
urlpatterns = [
    path('campaignhome/',CampaignView.as_view(),name="campaignhome"),
    path('createcampaign/',CampaignPostView.as_view(), name='postcampaign'),
    path('postcampaigncomment/',views.postcampaigncomment, name='postcampaigncomment'),
    path('initiatekhalti/', views.initiatekhalti, name='initiatekhalti'),
    path('verifykhalti/', views.verifykhalti, name='verifykhalti'),
    path('<slug:slug>/', CampaignDetailView.as_view(), name='campaigndetail'),
    path('editcampaign/<slug:slug>/', CampaignEditView.as_view(), name='campaignedit'),
    path('deletecampaign/<slug:slug>/', views.deletecampaign, name='campaigndelete'),
    path('<slug:slug>/donate/', DonateFormView.as_view(), name='donate'),
    path('donation-details/<int:campaign_id>/', views.donation_details, name='donation_details'), 
    #path('<slug:slug>/donate/process/', DonateProcessView.as_view(), name='donate_process'),
]