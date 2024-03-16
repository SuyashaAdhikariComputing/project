from django.shortcuts import redirect, render, HttpResponse
from blog.models import Post
from django.contrib import messages
from django.shortcuts import get_object_or_404
# Create your views here.


def bloghome(request):
    allPosts = Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request, 'blog/bloghome.html', context)

def postcontent(request):
    if request.method=="POST":
        
        title=request.POST['title']
        content=request.POST['content'] 
        
        blog_post=Post(title=title, content=content, author=request.user)
        blog_post.save()
        messages.success(request, "sucessfully Posted")
        return redirect('bloghome')
    return render(request,'blog/blogform.html')

def blogpost(request, slug):
    post= Post.objects.filter (slug=slug).first()
    context={'post': post}
    return render(request,'blog/blogPost.html',context)

def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST":
        
        title = request.POST['title']
        content = request.POST['content'] 

        post.author = request.user
        post.title = title
        post.content = content
        post.save()
        messages.success(request, "Successfully updated")
        return redirect('blogpost', slug=slug)

    context = {'post': post}
    return render(request, 'blog/blogform.html', context)

def deleteblog(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    messages.success(request, "sucessfully deleted")
    return redirect('bloghome')