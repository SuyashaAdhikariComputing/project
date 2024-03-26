from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login as auth_login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from users.models import CustomUser as User
from blog.models import Post
from campaign.models import Campaign

from .forms import SignUpForm,LoginForm,PasswordChangeForm,EditProfileForm  # Import your Form
# Create your views here.

def signup(request):
    signup_form = SignUpForm(request.POST or None) 
    if request.method == 'POST':
         
         if signup_form.is_valid():
             signup_form.save()
             return redirect('login')  # Redirect to login after successful registration

     
    return render(request, "user/signup.html", {'signup_form': signup_form})

def user_login(request):
    login_form = LoginForm()

    if request.method == 'POST':
        login_form = LoginForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                return redirect('home')  # Redirect to profile on successful login

    return render(request, 'user/login.html', {'login_form': login_form})

@login_required
def profile(request):
    return render(request, 'user/profile.html')

def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def change_password(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            password_change_form.save()
            update_session_auth_hash(request, password_change_form.user)
            return redirect('profile')
    else:
         password_change_form = PasswordChangeForm(request.user)

    return render(request, 'user/changepassword.html', {'password_change_form': password_change_form})

@login_required
def edit_profile(request):
     user = request.user

     if request.method == 'POST':
         edit_form = EditProfileForm(request.POST, instance=user)
        
         if edit_form.is_valid():
             edit_form.save()
             return redirect('profile')
     else:
         edit_form = EditProfileForm(instance=user)

     return render(request, 'user/editprofile.html', {'edit_form': edit_form})


def all_user_view(request):
    if request.user.is_authenticated and request.user.role == 'employee':
        users = User.objects.all()
        donor_count = User.objects.filter(role='donor').count()
        organization_count = User.objects.filter(role='organization').count()
        total_blog_posts = Post.objects.all().count()
        total_campaign_posts = Campaign.objects.all().count()
        return render(request, 'admin/alluser.html', {
            'users': users, 
            'donor_count': donor_count, 
            'organization_count': organization_count,
            'total_blog_posts': total_blog_posts,
            'total_campaign_posts': total_campaign_posts,
            })
        
    else:
        
        return redirect('login')
    
def user_profile(request, user_id):
    # Fetch the user object based on the provided user_id
    user = get_object_or_404(User, id=user_id)
    
    # Render the user profile template with the user object
    return render(request, 'user/profile.html', {'user': user, 'current_user': request.user})