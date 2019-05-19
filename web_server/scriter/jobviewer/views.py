from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Q
from .models import Job


def home_page(request):
    return render(request, 'home.html')


def json_example(request):
    return render(request, 'json_example.html')


def chart_data(request):
    dataset = Job.objects

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'IDF by Keyword'},
        'series': [{
            'name': 'Aleph',
            'data': []
        }]
    }

    return JsonResponse(chart)

# def index(request):
#     return HttpResponse("Hello, world. Index page for jobviewer.")

