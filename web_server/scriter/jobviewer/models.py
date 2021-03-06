from django.db import models
from django.db.models.base import ModelBase


def create_model(db_table):

    class CustomMetaClass(ModelBase):
        def __new__(cls, name, bases, attrs):
            model = super(CustomMetaClass, cls).__new__(cls, name, bases, attrs)
            ## This db_table rename doesn't seem to have an effect
            # model._meta.db_table = db_table
            # model._meta.managed = False
            return model

    class CustomModel(models.Model):
        __metaclass__ = CustomMetaClass

        Keyword = models.CharField(max_length=100)
        TF = models.IntegerField()
        DF = models.IntegerField()
        IDF = models.FloatField()
        TFIDF = models.FloatField()
        DOCUMENT_COUNT = models.IntegerField()

    return CustomModel
