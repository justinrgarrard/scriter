from django.db import models


class Job(models.Model):
    # Temporary hard coded values
    class Meta:
        db_table = 'posting_statistics'
        managed = False

    Keyword = models.CharField(max_length=100)
    TF = models.IntegerField()
    DF = models.IntegerField()
    IDF = models.FloatField()
    TFIDF = models.FloatField()
    DOCUMENT_COUNT = models.IntegerField()
    JOB_TITLE = models.CharField(max_length=100)
