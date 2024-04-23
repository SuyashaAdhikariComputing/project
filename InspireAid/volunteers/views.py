from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
from django.shortcuts import render
from notification.models import Notification
from volunteers.models import VolunteerCampaign,Category,VolunteerCampaignComment,VolunteerApplication
from django.views.generic import ListView, DetailView, View, DeleteView
from django.contrib import messages

class VolunteerListView(ListView):
    model = VolunteerCampaign
    template_name = 'volunteer/volunteer_home.html'

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
            queryset = queryset.filter(end_date=date_query)
        if category_query:
            queryset = queryset.filter(categories__id=category_query)

        return queryset

class VolunteerCampaignDetailView(DetailView):
    model=VolunteerCampaign
    template_name='volunteer/volunteer_campaign_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_campaign = self.get_object()
        campaign_comments = VolunteerCampaignComment.objects.filter(campaign_post=current_campaign)
        user = self.request.user
        has_applied = False

        # Check if the user has applied for this campaign
        if user.is_authenticated:
            has_applied = current_campaign.volunteerapplication_set.filter(user=user).exists()

        context['volunteer_campaign'] = current_campaign
        context['campaign_comments'] = campaign_comments
        context['slug'] = current_campaign.slug
        context['has_applied'] = has_applied
        return context
    
class VolunteerCampaignPostView(View):
    template_name = 'volunteer/volunteer_campaign_form.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        return render(request, self.template_name, {'categories': categories})

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        description = request.POST.get('description')
        target_volunteers = request.POST.get('target_volunteers')
        category_id = request.POST.get('category')
        end_date = request.POST.get('end_date')
        image = request.FILES.get('image')
        
        category = Category.objects.get(pk=category_id)
        
        volunteer_campaign = VolunteerCampaign.objects.create(
            title=title,
            description=description,
            target_volunteers=target_volunteers,
            author=request.user,
            end_date=end_date,
            image=image
        )
        volunteer_campaign.categories.add(category)

        return redirect('volunteer-campaign-detail', pk=volunteer_campaign.pk)

class VolunteerCampaignEditView(View):
    template_name = 'volunteer/volunteer_campaign_form.html'

    def get(self, request, slug, *args, **kwargs):
        volunteer_campaign = get_object_or_404(VolunteerCampaign, slug=slug)
        categories = Category.objects.all()
        return render(request, self.template_name, {'volunteer_campaign': volunteer_campaign, 'categories': categories})

    def post(self, request, slug, *args, **kwargs):
        volunteer_campaign = get_object_or_404(VolunteerCampaign, slug=slug)
        
        title = request.POST.get('title')
        description = request.POST.get('description')
        target_volunteers = request.POST.get('target_volunteers')
        end_date = request.POST.get('end_date')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')

        volunteer_campaign.title = title
        volunteer_campaign.description = description
        volunteer_campaign.author = request.user
        volunteer_campaign.end_date = end_date

        # Check if target_volunteers is provided, otherwise keep the existing value
        if target_volunteers:
            volunteer_campaign.target_volunteers = target_volunteers

        # Check if category_id is provided, otherwise keep the existing category
        if category_id:
            category = Category.objects.get(pk=category_id)
            volunteer_campaign.categories.clear()
            volunteer_campaign.categories.add(category)

        # Check if image is provided, otherwise keep the existing image
        if image:
            volunteer_campaign.image = image
        else:
            # If image is not provided, set it to the existing image
            volunteer_campaign.image.save(volunteer_campaign.image.name, volunteer_campaign.image, save=False)

        volunteer_campaign.save()

        return redirect('volunteer-campaign-detail', pk=volunteer_campaign.pk)
    
def postvolunteercampaigncomment(request):
    if request.method == 'POST':
        # Extract comment, comment_author, and campaignid from the POST data
        comment_text = request.POST.get("comment")
        comment_author = request.user
        campaign_id = request.POST.get("campaignid")

        # Retrieve the volunteer campaign object
        campaign = get_object_or_404(VolunteerCampaign, pk=campaign_id)

        # Create a new VolunteerCampaignComment instance and save it
        comment = VolunteerCampaignComment(
            comment=comment_text,
            comment_author=comment_author,
            campaign_post=campaign
        )
        comment.save()

        messages.success(request, "Your comment has been posted successfully")

        # Redirect to the campaign detail page
        return redirect('volunteer-campaign-detail', pk=campaign_id)
    
def apply_for_volunteer(request, campaign_id):
    campaign = get_object_or_404(VolunteerCampaign, pk=campaign_id)
    user = request.user

    # Check if the user has already applied for this campaign
    if VolunteerApplication.objects.filter(user=user, campaign=campaign).exists():
        messages.error(request, "You have already applied for this campaign.")
        return redirect('volunteer-campaign-detail', pk=campaign_id)

    # If the user hasn't applied, create a new application
    else:
        application = VolunteerApplication(user=user, campaign=campaign)
        application.save()

    # Update the current_volunteers count in the campaign
        campaign.current_volunteers += 1
        campaign.save()

        message = f"An applicant named {user} has applied for volunteer in {campaign.title}"
        Notification.objects.create(recipient=campaign.author, message=message)
        messages.success(request, "You have successfully applied for this campaign.")
        return redirect('volunteer-campaign-detail', pk=campaign_id)

def remove_volunteer_application(request, campaign_id):
    if request.method == 'POST':
        user = request.user
        campaign = get_object_or_404(VolunteerCampaign, pk=campaign_id)
        # Check if the user has an application for the specified campaign
        application = get_object_or_404(VolunteerApplication, user=user, campaign=campaign)
        # Delete the application
        application.delete()

        campaign.current_volunteers -= 1
        campaign.save()

        message = f"An applicant named {user} has removed application for {campaign.title}"
        Notification.objects.create(recipient=campaign.author, message=message)
         

        messages.success(request, "You have successfully removed volunteer application.")
        return redirect('volunteer-campaign-detail', pk=campaign_id)
    

def volunteer_campaign_details(request, slug):
    # Retrieve the volunteer campaign object using the slug
    campaign = get_object_or_404(VolunteerCampaign, slug=slug)

    # Retrieve donation applications for the campaign
    applications = VolunteerApplication.objects.filter(campaign=campaign)
    remaining_volunteers = campaign.target_volunteers - campaign.current_volunteers

    # Render the template with the volunteer campaign details and applications
    return render(request, 'volunteer/applied_details.html', {'campaign': campaign, 'applications': applications, 'remaining_volunteers': remaining_volunteers})

def deletecampaign(request, slug):
    campaign = get_object_or_404(VolunteerCampaign, slug=slug)
    campaign.delete()
    
    return redirect('volunteer_home')
   
   