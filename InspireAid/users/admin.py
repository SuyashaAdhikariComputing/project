from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,OTPModel

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'role', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active', 'role',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'phone', 'role', 'bio','profile_picture')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'role', 'bio', 'password1', 'password2','profile_picture' ,'is_staff', 'is_active')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(OTPModel)