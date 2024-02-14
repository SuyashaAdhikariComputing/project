from django.urls import path, include
from home import views

urlpatterns = [
    path('contact',views.Contact, name='contact'),
    path('about',views.about, name='about'),
    path('',views.home, name='home'),
]