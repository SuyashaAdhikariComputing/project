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
        def save(self, *args, **kwargs):

            if not self.author_id:
                # If author is not specified, assign a default user
                self.author = User.objects.first()  # You may adjust this logic based on your requirements
            
            if not self.slug:
                # Combine title, author username, and publish date to generate slug
                publish_date = timezone.now()  # Get the current date and time
                slug_text = f"{self.title} {self.author.username if self.author else 'unknown'} {publish_date.strftime('%Y-%m-%d %H:%M:%S')}"
                self.slug = slugify(slug_text)[:130]  # Limit slug length to 130 characters

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title