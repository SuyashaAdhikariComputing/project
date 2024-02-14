from django.shortcuts import render, HttpResponse

# Create your views here.


def bloghome(request):
    return HttpResponse('This is bloghome. we will keep all blog here')

def blogpost(request, slug):
    return HttpResponse(f'This is bloghome: {slug}')