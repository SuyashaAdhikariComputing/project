# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    ROLE_CHOICES = [
        ('donor', 'Donor'),
        ('organization', 'Organization'),
    ]
    
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username
    
