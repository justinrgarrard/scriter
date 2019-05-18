from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    return render(request, 'home.html')


# def index(request):
#     return HttpResponse("Hello, world. Index page for jobviewer.")

