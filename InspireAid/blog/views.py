from django.shortcuts import render, HttpResponse
from blog.models import Post
from django.contrib import messages
# Create your views here.


def bloghome(request):
    allPosts=Post.objects.all()
    context= {'allPosts': allPosts}
    return render(request,'blog/bloghome.html',context)

def postcontent(request):
    if request.method=="POST":
        author=request.POST['author']
        title=request.POST['title']
        content=request.POST['content'] 
        print(author, title, content)
        blog_post=Post(title=title, content=content, author=author)
        blog_post.save()
    return render(request,'blog/blogform.html')

def blogpost(request, slug):
    post= Post.objects.filter (slug=slug).first()
    context={'post': post}
    return render(request,'blog/blogPost.html',context)