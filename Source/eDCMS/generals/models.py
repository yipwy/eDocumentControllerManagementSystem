from django.db import models
from datetime import datetime


# Create your models here.
class DocumentType(models.Model):
    class Meta:
        verbose_name_plural     = 'Document_Types'
    document_code               = models.CharField(max_length=5)
    document_description        = models.CharField(max_length=50)
    document_number_seriesId    = models.CharField(max_length=30)
    is_active                   = models.BooleanField(default=False)
    created_by                  = models.CharField(max_length=20)
    created_date                = models.DateTimeField(default=datetime.now(), blank=True)
    modify_by                   = models.CharField(max_length=20)
    modify_date                 = models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self):
        return self.companyId
# Create your models here.
