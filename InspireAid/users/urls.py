from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    path('signup/', views.signup, name="signup"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name="logout"),
    path('campaigns/', views.campaign_list, name='campaign_list'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('profile/', views.profile, name="profile"),
    path('logout/', views.logout, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('user-list/', views.all_user_view, name='employee_user_list'),
    path('donation/history/', views.history, name='donation_history'),
    path('verify-email/<str:email>/', views.verify_user_mail, name='verify_user_mail'),
    path('user-profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('user/<int:user_id>/blogs/', views.user_blogs, name='user_blogs'),
    path('user/<int:user_id>/campaigns/', views.user_campaigns, name='user_campaigns'),
]