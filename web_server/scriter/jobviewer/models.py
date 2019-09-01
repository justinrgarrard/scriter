from django.db import models


class Job(models.Model):
    # Temporary hard coded values
    class Meta:
        db_table = 'software_engineer'
        managed = False

    Keyword = models.CharField(max_length=100)
    TF = models.IntegerField()
    DF = models.IntegerField()
    IDF = models.FloatField()
    TFIDF = models.FloatField()
    DOCUMENT_COUNT = models.IntegerField()
