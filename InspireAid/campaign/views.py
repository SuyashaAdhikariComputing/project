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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the current campaign object
        current_campaign = self.get_object()

        # Get three recommended campaigns (you may customize this logic based on your requirements)
        recommended_campaigns = Campaign.objects.exclude(pk=current_campaign.pk)[:3]

        context['recommended_campaigns'] = recommended_campaigns
        return context