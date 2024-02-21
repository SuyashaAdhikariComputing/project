from django.shortcuts import render, HttpResponse
from home.models import contact
from django.contrib import messages
# Create your views here.


def home(request):
    return render(request,'home/home.html')

def Contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        
        if name==''or len(email)<3 or len(phone)<10 or len(content)<6:
            messages.error(request,"Fill form corectly")

        else:
            Contact_value=contact(name=name, email=email, phone=phone, content=content)
            Contact_value.save()
            messages.success(request, "Messege sent sucessfully")

    return render(request,'home/contact.html')# go to contact page

def about(request):
    return HttpResponse('This is about')