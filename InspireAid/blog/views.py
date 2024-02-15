from django.shortcuts import render, HttpResponse
from blog.models import Post
# Create your views here.


def bloghome(request):
    allPosts=Post.objects.all()
    context= {'allPosts': allPosts}
    return render(request,'blog/bloghome.html')

def blogpost(request, slug):
    return HttpResponse(f'This is bloghome: {slug}')