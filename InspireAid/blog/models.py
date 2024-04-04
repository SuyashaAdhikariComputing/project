from django.db import models
from django.utils.text import slugify
from users.models import CustomUser as User
from ckeditor.fields import RichTextField
# Create your models here.

class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    #content=RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to='myimage/', null=True, blank=True)  # New field for image uploads
    content=models.TextField()
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    slug=models.CharField(max_length=130,unique=True, blank=True)
    timestamp=models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
         return f"{self.title} by {self.author.username}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate slug using title and author
            self.slug = slugify(f"{self.title} {self.author}")
        super().save(*args, **kwargs)

class BlogComment(models.Model):
    sno=models.AutoField(primary_key= True)
    comment = models.TextField()
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    Blog_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now_add=True, blank=True)
    parent=models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.comment[0:13]+"...."+"by "+ self.comment_author.first_name