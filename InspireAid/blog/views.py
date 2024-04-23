from django.shortcuts import redirect, render, HttpResponse
from blog.models import Post,BlogComment
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
        image = request.FILES.get('image')

        if not (title and content):
            messages.error(request, "Title and content fields cannot be empty.")
            return render(request, 'blog/blogform.html', {'error_messages': messages.get_messages(request)})
        
        blog_post=Post(title=title, image=image, content=content, author=request.user)
        blog_post.save()
        messages.success(request, "sucessfully Posted")
        return redirect('bloghome')
    return render(request,'blog/blogform.html')

def blogpost(request, slug):
    post= Post.objects.filter (slug=slug).first()
    comments=BlogComment.objects.filter(Blog_post=post)
    context={'post': post, 'comments':comments}
    return render(request,'blog/blogPost.html',context)

def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST":
        
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES.get('image')

        if image:
            post.image = image 

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

def postcomment(request):
    if request.method == 'POST':
        
        comment = request.POST.get("comment")
        comment_author = request.user
        postSno = request.POST.get("postSno")
        post=get_object_or_404(Post, sno=postSno)

        comment= BlogComment(comment=comment, comment_author=comment_author, Blog_post=post)
        comment.save()
        messages.success(request, "Your Comment has been posted sucessfully")
    
        return redirect('blogpost', slug=post.slug)
