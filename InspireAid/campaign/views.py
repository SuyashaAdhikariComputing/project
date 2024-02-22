from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Campaign
# Create your views here.

class CampaignView(ListView):
    model=Campaign
    template_name='campaign/campaignhome.html'

class CampaignDetailView(DetailView):
    model=Campaign
    template_name='campaign/campaignDetail.html'

    