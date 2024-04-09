from datetime import timezone
from django.db import models

# Create your models here.
from django.db import models
from users.models import CustomUser as User
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class VolunteerCampaign(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    target_volunteers = models.IntegerField()
    current_volunteers = models.IntegerField(default=0)
    publish_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='volunteer_campaigns', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=130, unique=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='volunteer_campaigns')
    image = models.ImageField(upload_to='volunteer_campaign_images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate a unique slug based on the campaign title
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while VolunteerCampaign.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class VolunteerCampaignComment(models.Model):
    sno=models.AutoField(primary_key= True)
    comment = models.TextField()
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign_post = models.ForeignKey(VolunteerCampaign, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now_add=True, blank=True)
    parent=models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.comment[0:13]+"...."+"by "+ self.comment_author.first_name
    
class VolunteerApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey(VolunteerCampaign, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'campaign')

    def __str__(self):
        return f"{self.user.username} applied for {self.campaign.title}"