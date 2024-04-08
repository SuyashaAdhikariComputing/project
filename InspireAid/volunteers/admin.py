from django.contrib import admin

# Register your models here.

from  volunteers.models import VolunteerCampaign,Category
# Register your models here.
admin.site.register(VolunteerCampaign)
admin.site.register(Category)
