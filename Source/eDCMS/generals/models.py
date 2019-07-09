from django.db import models
from datetime import datetime


class DocumentType(models.Model):
    class Meta:
        verbose_name_plural = 'DocumentTypes'

    document_code = models.CharField(max_length=5)
    document_description = models.CharField(max_length=50)
    document_number_seriesId = models.ForeignKey('SeriesNumber', null=True, blank=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    created_by = models.CharField(max_length=20)
    created_date = models.DateTimeField(default=datetime.now(), blank=True)
    modify_by = models.CharField(max_length=20)
    modify_date = models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self):
        return self.document_description


class SeriesNumber(models.Model):
    class Meta:
        verbose_name_plural = 'Series_Numbers'

    series_code = models.CharField(max_length=5)
    series_description = models.CharField(max_length=50)
    starting_number = models.IntegerField()
    ending_number = models.IntegerField()
    next_number = models.IntegerField()
    is_active = models.BooleanField(default=False)
    created_by = models.CharField(max_length=20)
    created_date = models.DateTimeField(default=datetime.now(), blank=True)
    modify_by = models.CharField(max_length=20)
    modify_date = models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self):
        return self.series_description
