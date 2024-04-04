from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login as auth_login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from users.models import CustomUser as User
from blog.models import Post
from campaign.models import Campaign
from django.core.mail import send_mail
from users.models import OTPModel
from .forms import SignUpForm,LoginForm,PasswordChangeForm,EditProfileForm,VerificationForm  # Import your Form
# Create your views here.
from django.contrib import messages
import random
from django.conf import settings

def otp_generation():
    return str(random.randint(100000, 999999))


def send_email(email, otp):
    title = 'Email Verification OTP'
    content = f'The OTP for mail verification is: {otp}'
    email_from = settings.EMAIL_HOST_USER 
    reciever=[email] 
    send_mail(title, content, email_from, reciever)

def signup(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)

        if signup_form.is_valid():
            username = signup_form.cleaned_data['username']
            email = signup_form.cleaned_data['email']
            phone = signup_form.cleaned_data['phone']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')

            elif User.objects.filter(email=email).exists():
                messages.error(request, 'This email already have account')

            elif User.objects.filter(phone=phone).exists():
                messages.error(request, 'This phone number is already registered')

            else:
                otp = otp_generation()
                user = signup_form.save(commit=False)
                user.is_active = False
                user.save()

                otp_model = OTPModel(user=user, otp=otp)
                otp_model.save()

                send_email(email, otp)
                
                return redirect('verify_user_mail', email=email)
        else:
            messages.error(request, 'fill all fields ')
    else:
        signup_form = SignUpForm()
    
    return render(request, "user/signup.html", {'signup_form': signup_form})

    # signup_form = SignUpForm(request.POST or None) 
    # if request.method == 'POST':
         
    #      if signup_form.is_valid():
    #          signup_form.save()
    #          return redirect('login')  # Redirect to login after successful registration

     
    # return render(request, "user/signup.html", {'signup_form': signup_form})

def verify_user_mail(request, email):
    if request.method == 'POST':
        otp_form = VerificationForm(request.POST)
        if otp_form.is_valid():
            otp = otp_form.cleaned_data['otp']
            try:
                user = User.objects.get(email=email)
                otp_model = OTPModel.objects.get(user=user)
                if otp == otp_model.otp:
                    otp_model.delete()
                    user.is_active = True
                    user.save()
                    return redirect('login')
                else:
                    messages.ERROR(request, 'The otp is not correct')

            except OTPModel.DoesNotExist:
                messages.ERROR(request, 'OTP is not send')
                
            except User.DoesNotExist:
                messages.ERROR(request, 'User with this email does not exist')


    else:
        otp_form = VerificationForm()

    return render(request, "user/token.html",  {'otp_form': otp_form, 'email': email})



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
        edit_form = EditProfileForm(request.POST, request.FILES, instance=user)  # Pass request.FILES for file data
        
        if edit_form.is_valid():
            # Save the form without profile_picture field
            edit_form.save(commit=False)
            
            # Handle profile_picture separately
            profile_picture = request.FILES.get('profile_picture')
            if profile_picture:
                user.profile_picture = profile_picture
                user.save()

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
    
def user_profile(request, user_id):#to get the user profile of the user by the employee
    # Fetch the user object based on the provided user_id
    user = get_object_or_404(User, id=user_id)
    
    # Render the user profile template with the user object
    return render(request, 'user/profile.html', {'user': user, 'current_user': request.user})

@login_required
def delete_user(request, user_id):
    # Fetch the user object based on the provided user_id
    user = get_object_or_404(User, id=user_id)
    
    # Check if the request method is POST
    if request.method == 'POST':
        # Delete the user
        user.delete()
        # Display a success message
        messages.success(request, 'User deleted successfully.')
    
    # Redirect back to the user list page
    return redirect('employee_user_list')