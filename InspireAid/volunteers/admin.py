from django.contrib import admin

# Register your models here.

from  volunteers.models import VolunteerCampaign,Category,VolunteerApplication
# Register your models here.
admin.site.register(VolunteerCampaign)
admin.site.register(Category)
admin.site.register(VolunteerApplication)
