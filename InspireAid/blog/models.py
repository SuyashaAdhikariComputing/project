from django.db import models
from django.utils.text import slugify
from users.models import CustomUser as User
# Create your models here.

class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    content=models.TextField()
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    slug=models.CharField(max_length=130,unique=True, blank=True)
    timestamp=models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title + ' by ' + self.author
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate slug using title and author
            self.slug = slugify(f"{self.title} {self.author}")
        super().save(*args, **kwargs)
