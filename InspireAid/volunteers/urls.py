
from django.urls import path, include
from . views import VolunteerListView
from volunteers import views
urlpatterns = [
    path('volunteer_home/',VolunteerListView.as_view(),name="volunteer_home"),
    
]