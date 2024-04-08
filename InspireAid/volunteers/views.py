from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from volunteers.models import VolunteerCampaign
from django.views.generic import ListView, DetailView, View, DeleteView


class VolunteerListView(ListView):
    model=VolunteerCampaign
    template_name='volunteer/volunteer_home.html'