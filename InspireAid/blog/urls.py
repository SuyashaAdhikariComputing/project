
from django.urls import path, include
from blog import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('bloghome/',views.bloghome, name='bloghome'),
    path('createblog/',views.postcontent, name='postcontent'),
    path('postcomment/',views.postcomment, name='postcomment'),
    path('<str:slug>/',views.blogpost, name='blogpost'),
    path('editblog/<slug:slug>/', views.edit_post, name='editblog'),
    path('deleteblog/<slug:slug>/', views.deleteblog, name='deleteblog'),#path
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)