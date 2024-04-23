
from decimal import Decimal
import json
from notification.models import Notification
from django.http import HttpResponseRedirect
from .models import Donation
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy,reverse
from django.views.generic import ListView, DetailView, View, DeleteView
import requests
import urllib3
from .models import Campaign,CampaignComment
from volunteers.models import Category
# Create your views here.

class CampaignView(ListView):
    model=Campaign
    template_name='campaign/campaignhome.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Get all categories
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        name_query = self.request.GET.get('name')
        date_query = self.request.GET.get('date')
        category_query = self.request.GET.get('category')

        if name_query:
            queryset = queryset.filter(title__icontains=name_query)
        if date_query:
            queryset = queryset.filter(created_at__date=date_query)
        if category_query:
            queryset = queryset.filter(category_id=category_query)

        return queryset

class CampaignDetailView(DetailView):
    model=Campaign
    template_name='campaign/campaignDetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the current campaign object
        current_campaign = self.get_object()

        

        campaign_comments = CampaignComment.objects.filter(campaign_post=current_campaign.pk)

        
        context['campaign_comments'] = campaign_comments
        return context
    
class CampaignPostView(View):

    template_name = 'campaign/campaignform.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()  # Get all categories
        context = {'categories': categories}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        categories = Category.objects.all() 
        context = {'categories': categories}
        # Retrieve data from POST request
        title = request.POST.get('title')
        description = request.POST.get('content')
        target_amount = request.POST.get('amount')
        image = request.FILES.get('image')
        category_id = request.POST.get('category')

        if not (title and description and target_amount):
            messages.error(request, 'Title, content, and target amount are required.')
            return render(request, self.template_name, {'error_messages': messages.get_messages(request), 'context': context})
        elif not target_amount.isdecimal():
            messages.error(request, 'Invalid target amount format. Please provide a valid decimal value.')
            return render(request, self.template_name, {'error_messages': messages.get_messages(request), 'context': context})
        elif Decimal(target_amount) <= 10:
            messages.error(request, 'Target amount must be greater than 10.')
            return render(request, self.template_name, {'error_messages': messages.get_messages(request), 'context': context})

        else:
             Campaign.objects.create(
                title=title,
                description=description,
                target_amount=target_amount,
                image=image,
                author=request.user,
                category_id=category_id
            )

        # Redirect to success URL
        return redirect('/campaign/campaignhome/')
    
class CampaignEditView(View):
    template_name = 'campaign/campaignform.html'

    def get(self, request, slug, *args, **kwargs):
        campaign = get_object_or_404(Campaign, slug=slug)
        categories = Category.objects.all()  # Get all categories
        context = {'campaign': campaign, 'categories': categories}
        return render(request, self.template_name, context)

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

        category_id = request.POST.get('category')
        campaign.category_id = category_id
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
    
def check_amount_limit(request):

    purchase_order_id = request.POST.get('campaign_id')
    given_amount=Decimal(request.POST.get('amount'))
    amount=(given_amount/100)

    campaign = Campaign.objects.get(id=purchase_order_id)
    total_capacity = campaign.target_amount
    current_amount = campaign.current_amount
    current_capacity=total_capacity-current_amount

    if amount <= 1000 and amount >= 10:

        if amount < 0:
          messages.error(request, 'Donation amount cannot be negative.')
          return redirect('campaigndetail', slug=campaign.slug)

        elif current_capacity >= amount:
            return initiatekhalti(request)
        
        else:
            messages.error(request, f'Donation amount exceeds total campaign capacity So, you cant donate more than {current_capacity} ')
            return redirect('campaigndetail', slug=campaign.slug)
    else:
        messages.error(request, ' you cant donate more than Rs 1000 or more than Rs 10 ')
        return redirect('campaigndetail', slug=campaign.slug)


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
        "name": user.first_name if user.first_name else "Anonymous",
        "email": user.email,
        "phone": user.phone
        }
    })
    headers = {
        'Authorization': 'key e53ede9bcdc74b6aa0b307c2f8785aa5',
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
         'Authorization': 'key e53ede9bcdc74b6aa0b307c2f8785aa5',
         'Content-Type': 'application/json',
         }

          pidx= request.GET.get('pidx')
          campaign_id= request.GET.get('purchase_order_id')
          amount=request.GET.get('amount')
          

          data=json.dumps({
             'pidx':pidx
          })

          res = requests.request("POST", url, headers=headers, data=data)
          print(res)
          print(res.text)

          new_res=json.loads(res.text)
          print(new_res)
         
          donor_amount= Decimal(amount) / Decimal(100)
    
          if new_res['status']== 'Completed':
              donation = Donation.objects.create(
                 campaign_id=campaign_id,
                 user_id=request.user.id,
                 amount=donor_amount
              )

              donation.save()

              campaign = get_object_or_404(Campaign, id=campaign_id)
              campaign.current_amount += Decimal(amount) / Decimal(100)
              campaign.save()

              campaign_owner = campaign.author

              # Notification creation
              message = f"A donation of {donor_amount} Rs. has been made to your campaign: {campaign.title}"
              Notification.objects.create(recipient=campaign_owner, message=message)
         
          return render(request, 'donation/sucess_page.html')
        
def donation_details(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    remaining_amount = campaign.target_amount - campaign.current_amount
    return render(request, 'campaign/campaign_donation.html', {'campaign': campaign, 'remaining_amount': remaining_amount})