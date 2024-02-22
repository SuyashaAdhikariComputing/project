from django.db import models
from django.utils.text import slugify

# Create your models here.

class Campaign(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    slug=models.CharField(max_length=130,unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate slug using title and author
            self.slug = slugify(f"{self.title}")
        super().save(*args, **kwargs)
