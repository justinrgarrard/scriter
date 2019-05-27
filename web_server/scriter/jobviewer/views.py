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
    print(list(dataset.values_list('Keyword', flat=True)))

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'TFIDF by Keyword'},
        'xAxis': {'categories': list(dataset.values_list('Keyword', flat=True))},
        'series': [{
            'name': 'TFIDF',
            'data': list(dataset.values_list('TFIDF', flat=True))
        }]
    }

    return JsonResponse(chart)

# def index(request):
#     return HttpResponse("Hello, world. Index page for jobviewer.")

