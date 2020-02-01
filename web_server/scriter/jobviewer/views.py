import numpy as np
from django.shortcuts import render
from django.http import JsonResponse
from .models import create_model


def home_page(request):
    return render(request, 'index.html')


def job_json(request):
    return render(request, 'index.html')


def chart_data(request):
    # Queried object
    params = request.GET
    job_table = params['job'].replace(' ', '_').lower()
    Job = create_model(job_table)
    Job._meta.db_table = job_table
    dataset = Job.objects

    # Query string parameters
    job = params['job']
    metric = params['metric']
    sort_style = params['sortstyle']

    # Pull chart info from the query set and query string
    record_count = list(dataset.values_list('DOCUMENT_COUNT', flat=True))[-1]
    keys = list(dataset.values_list('Keyword', flat=True))
    vals = list(dataset.values_list(metric, flat=True))
    matched = list(zip(keys, vals))

    title = '{0} Keywords'.format(job)
    subtitle = 'Record Count = {0}'.format(record_count)

    if sort_style == 'ordered':
        # Sort by Val, least to most
        matched = sorted(matched, key=lambda x: x[1])
    else:
        # Sort by Key, alphabetically
        matched = sorted(matched, key=lambda x: x[0])

    ## Ignore keys below the first quartile for easier viewing
    cutoff = np.percentile(vals, 25)
    matched = [(item[0], item[1]) for item in matched if item[1] > cutoff]

    ## Remove any zero value items
    matched = [(item[0], item[1]) for item in matched if item[1] > 0]

    # Map metric to color
    color_matcher = {'TFIDF': '#7cb5ec', 'TF': '#f79039', 'DF': '#90ed7d', 'IDF': '#8085e9'}

    # Break zipped list back into keys and values
    keys_matched = [x[0] for x in matched]
    vals_matched = [x[1] for x in matched]

    # Generate the chart
    chart = {
        'chart': {'type': 'column'},
        'title': {'text': title},
        'subtitle': {'text': subtitle},
        'xAxis': {'categories': keys_matched},
        'plotOptions': {'series': {'color': color_matcher[metric]}},
        'series': [{
            'name': metric,
            'data': vals_matched
        }]
    }
    return JsonResponse(chart)

