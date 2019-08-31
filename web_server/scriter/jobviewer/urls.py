from django.urls import path

from . import views

urlpatterns = [
    path('json-example/', views.job_json, name='json_example'),
    path('json-example/data/', views.chart_data, name='chart_data'),
]