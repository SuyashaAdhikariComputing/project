from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login as auth_login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from users.models import CustomUser as User
from blog.models import Post
from volunteers.models import VolunteerCampaign,Category
from campaign.models import Campaign,Donation
from django.core.mail import send_mail
from users.models import OTPModel
from .forms import SignUpForm,LoginForm,PasswordChangeForm,EditProfileForm,VerificationForm  # Import your Form
# Create your views here.
from django.contrib import messages
import random
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def otp_generation():
    return str(random.randint(100000, 999999))


def send_email(email, otp):
    title = 'Email Verification OTP'
    content = f'The OTP for mail verification is: {otp}'
    email_from = settings.EMAIL_HOST_USER 
    reciever=[email] 
    send_mail(title, content, email_from, reciever)

# def signup(request):
#     if request.method == 'POST':
#         signup_form = SignUpForm(request.POST)

#         if signup_form.is_valid():
#             username = signup_form.cleaned_data['username']
#             email = signup_form.cleaned_data['email']
#             phone = signup_form.cleaned_data['phone']

            
#             otp = otp_generation()
#             user = signup_form.save(commit=False)
#             user.is_active = False
#             user.save()

#             otp_model = OTPModel(user=user, otp=otp)
#             otp_model.save()

#             send_email(email, otp)
                
#             return redirect('verify_user_mail', email=email)
#         else:
#              for field, errors in signup_form.errors.items():
#                 for error in errors:
#                     messages.error(request, f"Error in field '{field}': {error}")
#     else:
#         signup_form = SignUpForm()
       
    
#     error_messages = [message.message for message in messages.get_messages(request)]
    
#     print(error_messages)
#     return render(request, "user/signup.html", {'signup_form': signup_form, 'error_messages': error_messages})

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
                messages.error(request, 'This email already has an account.')

            elif User.objects.filter(phone=phone).exists():
                messages.error(request, 'This phone number is already registered.')

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
            for field, errors in signup_form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in field '{field}': {error}")
    else:
        signup_form = SignUpForm()
        

    error_messages = [message.message for message in messages.get_messages(request)]

    print(error_messages)

    return render(request, "user/signup.html", {'signup_form': signup_form, 'error_messages': error_messages})

    
    

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
                    messages.error(request, 'The otp is not correct')

            except OTPModel.DoesNotExist:
                messages.error(request, 'OTP is not send')
                
            except User.DoesNotExist:
                messages.error(request, 'User with this email does not exist')


    else:
        otp_form = VerificationForm()
    
    error_messages = [message.message for message in messages.get_messages(request)]

    return render(request, "user/token.html",  {'otp_form': otp_form, 'email': email, 'error_messages': error_messages})


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Get the email directly from request.POST
        if not email:
            messages.error(request, 'give email to change pasword')

        else:

        # Check if the email exists in the database
          user = User.objects.filter(email=email).first()
        
        if user:
            otp = otp_generation()
            otp_model = OTPModel(user=user, otp=otp)
            otp_model.save()
            send_email(email, otp)
            
            return redirect('verify_password_reset', email=email)
        else:
            messages.error(request, 'No user found with this email address.')
        
    error_messages = [message.message for message in messages.get_messages(request)]
    
   
    
    # If the request method is not POST or there was an error, render the form
    return render(request, 'user/forgotpassword.html',{'error_messages': error_messages})


def verify_password_reset(request, email):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            otp_model = OTPModel.objects.filter(user__email=email).first()
            if otp_model and otp == otp_model.otp:
                otp_model.delete()
                
                user = User.objects.filter(email=email).first()
                if user:
                    return redirect('password_reset', email=email)
                else:
                    return HttpResponseServerError('User not found.')
                
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
        form = VerificationForm()

    error_messages = [message.message for message in messages.get_messages(request)]

    return render(request, 'user/forgot_token.html', {'otp_form': form, 'email': email, 'error_messages': error_messages})

def password_reset(request, email):
    if request.method == 'POST':
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        if new_password1 != new_password2:
            messages.error(request, "Passwords don't match.")
            return redirect('reset_password', email=email)

        user = User.objects.filter(email=email).first()
        if user:
            user.set_password(new_password1)
            user.save()
            messages.success(request, 'Your password has been successfully changed. Please login with your new password.')
            return redirect('login')
        else:
            return HttpResponseServerError('User not found.')
        
    error_messages = [message.message for message in messages.get_messages(request)]


    return render(request, 'user/password_reset.html', {'email': email, 'error_messages': error_messages})


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
            else:
                messages.error(request, 'Invalid username or password.')  # Error message for invalid credentials
                return redirect('login')
        else:
            for field, errors in login_form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in field : {error}")  # Error message for form validation errors

    error_messages = [message.message for message in messages.get_messages(request)]
    return render(request, 'user/login.html', {'login_form': login_form,'error_messages': error_messages})

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
            new_password1 = password_change_form.cleaned_data['new_password1']
            new_password2 = password_change_form.cleaned_data['new_password2']

            if new_password1 != new_password2:
                messages.error(request, "Passwords don't match.")
            else:
                password_change_form.save()
                update_session_auth_hash(request, password_change_form.user)
                return redirect('profile')
        else:
            for field, errors in password_change_form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in field : {error}")
    else:
         password_change_form = PasswordChangeForm(request.user)

    error_messages = [message.message for message in messages.get_messages(request)]

    return render(request, 'user/changepassword.html', {'password_change_form': password_change_form, 'error_messages': error_messages})

@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        edit_form = EditProfileForm(request.POST, request.FILES, instance=user)
        
        if edit_form.is_valid():
            edit_form.save(commit=False)
            
            profile_picture = request.FILES.get('profile_picture')
            if profile_picture:
                user.profile_picture = profile_picture
                user.save()

            return redirect('profile')
        else:
            for field, errors in edit_form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in field : {error}")
    else:
        edit_form = EditProfileForm(instance=user)
        

    error_messages = [message.message for message in messages.get_messages(request)]

    return render(request, 'user/editprofile.html', {'edit_form': edit_form, 'error_messages': error_messages})


def all_user_view(request):
    if request.user.is_authenticated and request.user.role == 'employee':
        users = User.objects.all()

        role_filter = request.GET.get('role')
        if role_filter:
            users = users.filter(role=role_filter)

        search_query = request.GET.get('search')
        if search_query:
            users = users.filter(username__icontains=search_query)

        user_count = (User.objects.filter(role='organization').count() + User.objects.filter(role='donor').count())
        total_blog_posts = Post.objects.all().count()
        total_campaign_posts = Campaign.objects.all().count()
        total_volunteer_posts = VolunteerCampaign.objects.all().count()

        return render(request, 'admin/alluser.html', {
            'users': users, 
            'user_count': user_count,
            'total_blog_posts': total_blog_posts,
            'total_campaign_posts': total_campaign_posts,
            'total_volunteer_posts': total_volunteer_posts
        })
    else:
        return redirect('login')

    
def user_profile(request, user_id):#to get the user profile of the user by the employee
    
    user = get_object_or_404(User, id=user_id)
    
    
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

def history(request):
    # Get donations related to the logged-in user
    user_donations = Donation.objects.filter(user=request.user).order_by('-date')

    context = {
        'user_donations': user_donations
    }
    return render(request, 'user/history.html', context)

def user_blogs(request, user_id):
    user = get_object_or_404(User, id=user_id)
    blogs = Post.objects.filter(author=user)
    return render(request, 'user/created_blog.html', {'user': user, 'blogs': blogs})

def user_campaigns(request, user_id):
    user = get_object_or_404(User, id=user_id)
    campaigns = Campaign.objects.filter(author=user)
    return render(request, 'user/created_campaign.html', {'user': user, 'campaigns': campaigns})

def user_volunteer_campaigns(request, user_id):
    user = get_object_or_404(User, id=user_id)
    volunteer_campaigns = VolunteerCampaign.objects.filter(author=user)
    return render(request, 'user/created_volunteer_campaigns.html', {'user': user, 'volunteer_campaigns': volunteer_campaigns})

def campaign_list(request):
    title_filter = request.GET.get('title')
    date_filter = request.GET.get('date')
    category_filter = request.GET.get('category')

    campaigns = Campaign.objects.all()

    if title_filter:
        campaigns = campaigns.filter(title__icontains=title_filter)

    if date_filter:
        campaigns = campaigns.filter(created_at__date=date_filter)

    if category_filter:
        campaigns = campaigns.filter(category__name=category_filter)  # Use 'category' field instead of 'categories'

    categories = Category.objects.all()  # Retrieve all categories
    
    context = {
        'campaigns': campaigns,
        'categories': categories,
    }
    
    return render(request, 'admin/campaign_list.html', context)
    
   
def blog_list(request):
    title_filter = request.GET.get('title')
    date_filter = request.GET.get('date')

    blogs = Post.objects.all()

    if title_filter:
        blogs = blogs.filter(title__icontains=title_filter)

    if date_filter:
        blogs = blogs.filter(timestamp__date=date_filter)

    return render(request, 'admin/blog_list.html', {'blogs': blogs})


def category_list(request):
    categories = Category.objects.all()  
    return render(request, 'admin/catagory_list.html', {'categories': categories})

def volunteer_list(request):
    title_filter = request.GET.get('title')
    date_filter = request.GET.get('date')
    category_filter = request.GET.get('category')

    volunteers = VolunteerCampaign.objects.all()

    if title_filter:
        volunteers = volunteers.filter(title__icontains=title_filter)

    if date_filter:
        volunteers = volunteers.filter(created_at__date=date_filter)

    if category_filter:
        volunteers = volunteers.filter(categories__name=category_filter)

    categories = Category.objects.all()  # Get all categories for the dropdown menu

    context = {
        'volunteers': volunteers,
        'categories': categories,
    }

    return render(request, 'admin/volunteercampaign_list.html', context)

@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        if name and description:
            category = Category(name=name, description=description)
            category.save()
            messages.success(request, 'Category added successfully.')
            return redirect('category_list')
        else:
            messages.error(request, 'Error adding category. Please provide both name and description.')
    
    return render(request, 'admin/add_catagory.html')

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
    return redirect('category_list')