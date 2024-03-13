
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View, DeleteView
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
    
class CampaignPostView(View):

    template_name = 'campaign/campaignform.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        # Retrieve data from POST request
        title = request.POST.get('title')
        description = request.POST.get('content')
        target_amount = request.POST.get('amount')

        # Create Campaign object
        campaign = Campaign.objects.create(
            title=title,
            description=description,
            target_amount=target_amount
        )

        # Redirect to success URL
        return redirect('/campaign/campaignhome/')
    
class CampaignEditView(View):
    template_name = 'campaign/campaignform.html'

    def get(self, request, slug, *args, **kwargs):
        campaign = get_object_or_404(Campaign, slug=slug)
        return render(request, self.template_name, {'campaign': campaign})

    def post(self, request, slug, *args, **kwargs):
        campaign = get_object_or_404(Campaign, slug=slug)

        campaign.title = request.POST.get('title')
        campaign.description = request.POST.get('content')
        campaign.target_amount = request.POST.get('amount')
        campaign.save()

        return redirect('/campaign/campaignhome/')


def deletecampaign(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    campaign.delete()
    
    return redirect('campaignhome')