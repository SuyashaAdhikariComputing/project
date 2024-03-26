
import uuid
from django.db import models
from django.utils.text import slugify
from users.models import CustomUser as User
# Create your models here.

def get_default_author():
    return User.objects.last()

class Campaign(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='campaigns', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug=models.CharField(max_length=130,unique=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.author_id:
            self.author = User.objects.last()
        super().save(*args, **kwargs)

class CampaignComment(models.Model):
    sno=models.AutoField(primary_key= True)
    comment = models.TextField()
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign_post = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now_add=True, blank=True)
    parent=models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.comment[0:13]+"...."+"by "+ self.comment_author.first_name

class Donation(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='donations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation of {self.amount} to {self.campaign.title} by {self.user.username} on {self.date}"

    

