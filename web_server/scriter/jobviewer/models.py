from django.db import models


class Job(models.Model):
    KEYWORD = models.CharField(max_length=100)
    TF = models.IntegerField()
    DF = models.IntegerField()
    IDF = models.FloatField()
    TFIDF = models.FloatField()
    DOCUMENT_COUNT = models.IntegerField
