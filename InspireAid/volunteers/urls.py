
from django.urls import path, include
from . views import VolunteerListView,VolunteerCampaignDetailView,VolunteerCampaignEditView,VolunteerCampaignPostView
from volunteers import views
urlpatterns = [
    path('volunteer_home/',VolunteerListView.as_view(),name="volunteer_home"),
    path('postvolunteercampaigncomment/',views.postvolunteercampaigncomment, name='postvolunteercampaigncomment'),
    path('post_volunteer_campaign/', VolunteerCampaignPostView.as_view(), name='post_volunteer_campaign'),
    path('volunteer_campaign/<int:pk>/', VolunteerCampaignDetailView.as_view(), name='volunteer-campaign-detail'),
    path('edit_volunteer_campaign/<slug:slug>/', VolunteerCampaignEditView.as_view(), name='edit_volunteer_campaign'),
    path('volunteer/apply/<int:campaign_id>/', views.apply_for_volunteer, name='apply_for_volunteer'),
    path('volunteer/remove_application/<int:campaign_id>/', views.remove_volunteer_application, name='remove_volunteer_application'),
    path('volunteercampaign/<slug:slug>/', views.volunteer_campaign_details, name='volunteer_campaign_details'),
    path('volunteer_campaign_delete/<slug:slug>', views.deletecampaign, name='delete_volunteer_campaign'),
]