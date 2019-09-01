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
    vals = list(dataset.values_list('TFIDF', flat=True))
    matched = zip(keys, vals)

    # Sort by Key
    # sorted(matched, key=lambda x: x[0])

    # Sort by Val
    sorted(matched, key=lambda x: x[1])

    # Break zipped list back apart
    keys_matched = [x[0] for x in matched]
    vals_matched = [x[1] for x in matched]

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': title},
        'xAxis': {'categories': keys_matched},
        'series': [{
            'name': metric,
            'data': vals_matched
        }]
    }

    return JsonResponse(chart)

# def index(request):
#     return HttpResponse("Hello, world. Index page for jobviewer.")

