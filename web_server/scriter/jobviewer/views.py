from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Job


def home_page(request):
    return render(request, 'index.html')


def job_json(request):
    return render(request, 'index.html')


def chart_data(request):
    # Queried object
    dataset = Job.objects

    # Query string parameters
    params = request.GET
    job = params['job'].replace('+', ' ')
    metric = params['metric']
    sort_style = params['sortstyle']

    # Pull chart info from the query set and query string
    record_count = list(dataset.values_list('DOCUMENT_COUNT', flat=True))[-1]
    keys = list(dataset.values_list('Keyword', flat=True))
    vals = list(dataset.values_list(metric, flat=True))
    matched = list(zip(keys, vals))

    title = '{0} Keywords [{1}]'.format(job, metric)
    subtitle = 'Record Count = {0}'.format(record_count)

    if sort_style == 'ordered':
        # Sort by Val, least to most
        matched = sorted(matched, key=lambda x: x[1])
    else:
        # Sort by Key, alphabetically
        matched = sorted(matched, key=lambda x: x[0])

    # Break zipped list back into keys and values
    keys_matched = [x[0] for x in matched]
    vals_matched = [x[1] for x in matched]

    # Generate the chart
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

