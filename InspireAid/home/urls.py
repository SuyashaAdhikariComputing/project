from django.urls import path, include
from home import views

urlpatterns = [
    path('contact',views.Contact, name='contact'),
    path('',views.home, name='home'),
]