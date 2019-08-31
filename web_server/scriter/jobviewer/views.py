from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Q
from .models import Job


def home_page(request):
    return render(request, 'index.html')


def job_json(request):
    return render(request, 'index.html')


def chart_data(request):
    dataset = Job.objects
    metric = 'TFIDF'
    title = 'Software Engineer Keywords [{}]'.format(metric)
    keys = list(dataset.values_list('Keyword', flat=True))
    vals =list(dataset.values_list('TFIDF', flat=True))

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': title},
        'xAxis': {'categories': keys},
        'series': [{
            'name': metric,
            'data': vals
        }]
    }

    return JsonResponse(chart)

# def index(request):
#     return HttpResponse("Hello, world. Index page for jobviewer.")

