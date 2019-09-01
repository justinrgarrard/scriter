from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Job


def home_page(request):
    return render(request, 'index.html')


def job_json(request):
    return render(request, 'index.html')


def chart_data(request):
    dataset = Job.objects
    record_count = list(dataset.values_list('DOCUMENT_COUNT', flat=True))[-1]
    keys = list(dataset.values_list('Keyword', flat=True))
    vals = list(dataset.values_list('TFIDF', flat=True))
    matched = list(zip(keys, vals))
    metric = 'TFIDF'
    title = 'Software Engineer Keywords [{}]'.format(metric)
    subtitle = 'Record Count = {0}'.format(record_count)

    # Sort by Key
    # sorted(matched, key=lambda x: x[0])

    # Sort by Val
    matched = sorted(matched, key=lambda x: x[1])

    # Break zipped list back into keys and values
    keys_matched = [x[0] for x in matched]
    vals_matched = [x[1] for x in matched]

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': title},
        'subtitle': {'text': subtitle},
        'xAxis': {'categories': keys_matched},
        'series': [{
            'name': metric,
            'data': vals_matched
        }]
    }

    return JsonResponse(chart)

