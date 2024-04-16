from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    path('signup/', views.signup, name="signup"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name="logout"),
    path('campaigns/', views.campaign_list, name='campaign_list'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('add_category/', views.add_category, name='add_category'),
    path('category_list/', views.category_list, name='category_list'),
    path('volunteer_list/', views.volunteer_list, name='volunteer_list'),
    path('donation_list/', views.volunteer_list, name='donation_list'),
    path('profile/', views.profile, name="profile"),
    path('logout/', views.logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('change-password/', views.change_password, name='change_password'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('user-list/', views.all_user_view, name='all_user_view'),
    path('donation/history/', views.history, name='donation_history'),
    path('verify-email/<str:email>/', views.verify_user_mail, name='verify_user_mail'),
    path('category/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('user-profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('user/<int:user_id>/volunteer_campaigns/', views.user_volunteer_campaigns, name='user_volunteer_campaigns'),
    path('user/<int:user_id>/blogs/', views.user_blogs, name='user_blogs'),
    path('user/<int:user_id>/campaigns/', views.user_campaigns, name='user_campaigns'),
    path('verify-password-reset/<str:email>/', views.verify_password_reset, name='verify_password_reset'),
    path('reset-password/<str:email>/', views.password_reset, name='password_reset'),
]