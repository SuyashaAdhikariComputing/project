
from django.urls import path, include
from blog import views

urlpatterns = [
    path('bloghome/',views.bloghome, name='bloghome'),
     #path('<str:slug>',views.blogpost, name='blogpost'),

]