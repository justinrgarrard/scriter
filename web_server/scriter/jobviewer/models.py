from django.db import models


# class Passenger(models.Model):
#     name = models.CharField()
#     sex = models.CharField()
#     survived = models.BooleanField()
#     age = models.FloatField()
#     ticket_class = models.PositiveSmallIntegerField()
#     embarked = models.CharField()

class Job(models.Model):
    KEYWORD = models.CharField(max_length=100)
    TF = models.IntegerField()
    DF = models.IntegerField()
    IDF = models.FloatField()
    TFIDF = models.FloatField()
    DOCUMENT_COUNT = models.IntegerField
