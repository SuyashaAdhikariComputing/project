from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from .models import CustomUser
# class SignUpForm(forms.Form):
#     username = forms.CharField(label='Username', max_length=100)
#     first_name = forms.CharField(label='first_Name', max_length=100)
#     last_name = forms.CharField(label='last_Name', max_length=100)
#     email = forms.EmailField(label='Email address')
#     phone = forms.CharField(label='Phone Number', max_length=15)
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)
#     confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
#     user_type = forms.ChoiceField(label='Role', choices=[('organization', 'Organization'), ('donor', 'Donor')])

class SignUpForm(UserCreationForm):
    phone = forms.CharField(max_length=15, required=False)

    ROLE_CHOICES = [
        ('donor', 'Donor'),
        ('organization', 'Organization'),
    ]

    role = forms.ChoiceField(label='Role', choices=ROLE_CHOICES, required=False)
    

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name','email', 'phone', 'role',  'password1', 'password2']

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class ChangePasswordForm(PasswordChangeForm):
     class Meta:
         model = CustomUser

class EditProfileForm(forms.ModelForm):
     class Meta:
         model = CustomUser
         fields = ['username', 'phone', 'bio']