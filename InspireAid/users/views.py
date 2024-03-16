from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout

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