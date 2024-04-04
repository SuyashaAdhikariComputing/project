
import json
from .models import Donation
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy,reverse
from django.views.generic import ListView, DetailView, View, DeleteView
import requests
import urllib3
from .models import Campaign,CampaignComment
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
        

        campaign_comments = CampaignComment.objects.filter(campaign_post=current_campaign.pk)

        
        context['campaign_comments'] = campaign_comments
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
        image = request.FILES.get('image')

        # Create Campaign object
        campaign = Campaign.objects.create(
            title=title,
            description=description,
            target_amount=target_amount,
            image=image,
            author=request.user
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
        campaign.author=request.user
        if 'image' in request.FILES:
            # Delete the old image file from the storage
            campaign.image.delete()

            # Assign the new uploaded image
            campaign.image = request.FILES['image']

        
        campaign.save()

        return redirect('campaigndetail', slug=slug)


def deletecampaign(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    campaign.delete()
    
    return redirect('campaignhome')

class DonateFormView(View):
    template_name = 'donation/detailform.html'

    def get(self, request, slug, *args, **kwargs):
        campaign = get_object_or_404(Campaign, slug=slug)
        context = {'campaign': campaign}
        return render(request, self.template_name, context)
    
def postcampaigncomment(request):
    if request.method == 'POST':
        
        comment = request.POST.get("comment")
        comment_author = request.user
        postSno = request.POST.get("campaignid")
        post=get_object_or_404(Campaign, pk=postSno)

        comment= CampaignComment(comment=comment, comment_author=comment_author, campaign_post=post)
        comment.save()
        messages.success(request, "Your Comment has been posted sucessfully")
    
        return redirect('campaigndetail', slug=post.slug)


def initiatekhalti(request):
    
    url = "https://a.khalti.com/api/v2/epayment/initiate/"

    purchase_order_id=request.POST.get('campaign_id')
    amount=request.POST.get('amount')
    return_url=request.POST.get('return_url')

    #print("campaign_id",purchase_order_id)
    #print("amount",amount)
    #print("return_url",return_url)

    user=request.user

    payload = json.dumps({
        "return_url": return_url,
        "website_url": "https://127.0.0.1:8000/",
        "amount": amount,
        "purchase_order_id": purchase_order_id ,
        "purchase_order_name": "test",
        "customer_info": {
        "name": user.first_name,
        "email": user.email,
        "phone": user.phone
        }
    })
    headers = {
        'Authorization': 'key bc5f23918f7c47d49e5316a4550258ea',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    new_res=json.loads(response.text)
    print(new_res)

    return redirect(new_res['payment_url'])

def verifykhalti(request):
    

    url = "https://a.khalti.com/api/v2/epayment/lookup/"

    if request.method == 'GET':

          headers = {
         'Authorization': 'key bc5f23918f7c47d49e5316a4550258ea',
         'Content-Type': 'application/json',
         }

          pidx= request.GET.get('pidx')
          campaign_id= request.GET.get('purchase_order_id')
          amount= request.GET.get('amount')

          data=json.dumps({
             'pidx':pidx
          })

          res = requests.request("POST", url, headers=headers, data=data)
          print(res)
          print(res.text)

          new_res=json.loads(res.text)
          print(new_res)
         
          
    
          if new_res['status']== 'Completed':
              donation = Donation.objects.create(
                 campaign_id=campaign_id,
                 user_id=request.user.id,
                 amount=amount
              )

              donation.save()
         
          return redirect(reverse('campaignhome'))
        