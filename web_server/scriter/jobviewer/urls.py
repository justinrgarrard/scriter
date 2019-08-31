from django.urls import path

from . import views

urlpatterns = [
    path('job-json/', views.job_json, name='json_example'),
    path('job-json/data/', views.chart_data, name='chart_data'),
]