
from django.urls import path, include

from notification import views
urlpatterns = [

    path('usersnotification/', views.view_notifications, name='view_notifications'),
    path('notifications/delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),
]