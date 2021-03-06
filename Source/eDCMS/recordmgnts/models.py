from django.db import models
from simple_history.models import HistoricalRecords
from datetime import *
from ckeditor_uploader.fields import RichTextUploadingField


class Container(models.Model):
    class Meta:
        verbose_name_plural     = 'Containers'
    container_serial_number     = models.CharField(max_length=35, unique=True)
    container_description       = RichTextUploadingField()
    status                      = models.BooleanField(default=True)
    created_by                  = models.CharField(max_length=120)
    created_date                = models.DateTimeField(default=datetime.now, blank=True)
    modify_by                   = models.CharField(max_length=120)
    modify_date                 = models.DateTimeField(default=datetime.now, blank=True)
    warehouse                   = models.ForeignKey('generals.Warehouse', on_delete=models.CASCADE)
    bay                         = models.ForeignKey('generals.Bay', on_delete=models.CASCADE)
    row                         = models.CharField(max_length=10, null=True)
    column                      = models.CharField(max_length=10, null=True)
    department                  = models.CharField(max_length=55, null=True)
    history = HistoricalRecords(table_name='container_history')
    is_deleted                  = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.container_serial_number


class OrderHeader(models.Model):
    class Meta:
        verbose_name_plural     = 'Order Headers'
    doc_type                    = models.ForeignKey('generals.DocumentType', on_delete=models.CASCADE)
    doc_serial_number           = models.CharField(max_length=20, unique=True)
    created_by                  = models.CharField(max_length=120)
    department                  = models.CharField(max_length=55)
    branch                      = models.CharField(max_length=50)
    created_date                = models.DateTimeField(default=datetime.now, blank=True)


class OrderDetail(models.Model):
    class Meta:
        verbose_name_plural     = 'Order Details'
    header                   = models.ForeignKey(OrderHeader, on_delete=models.CASCADE)
    container                = models.ForeignKey(Container, on_delete=models.SET_NULL, null=True)
    barcode                  = models.CharField(max_length=35, null=True)


class ContainerInstance(models.Model):
    class Meta:
        verbose_name            = 'Transaction'
        verbose_name_plural     = 'Transactions'
    container = models.ForeignKey(Container, on_delete=models.SET_NULL, null=True)
    due_date  = models.DateField(null=True)
    user      = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    status    = models.BooleanField(null=True)
    email_sent = models.BooleanField(default=False, null=True)

    @property
    def is_overdue(self):
        if date.today() > self.due_date:
            return True
        return False
        
    def is_returned(self):
        if self.status is True:
            return 'Returned'
        else:
            return 'Not returned'
            
    is_returned.short_description = 'Status'
