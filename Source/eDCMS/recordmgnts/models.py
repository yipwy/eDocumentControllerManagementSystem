from django.db import models
from datetime import datetime
from simple_history.models import HistoricalRecords


class Container(models.Model):
    class Meta:
        verbose_name_plural     = 'Containers'
    container_serial_number     = models.CharField(max_length=20, unique=True)
    container_description       = models.CharField(max_length=100)
    status                      = models.BooleanField(default=False)
    created_by                  = models.CharField(max_length=20)
    created_date                = models.DateTimeField(default=datetime.now, blank=True)
    modify_by                   = models.CharField(max_length=20)
    modify_date                 = models.DateTimeField(default=datetime.now, blank=True)
    warehouse                   = models.ForeignKey('generals.Warehouse', on_delete=models.CASCADE)
    location                    = models.ForeignKey('generals.Location', on_delete=models.CASCADE)
    history = HistoricalRecords(table_name='container_history')
    # permissions = (
    #     ('view', 'View container'),
    #     ('edit', 'Edit container'),
    #     ('delete', 'Delete container'),
    #     ('add', 'Add container'),
    # )

    def __str__(self):
        return self.container_serial_number


class OrderHeader(models.Model):
    class Meta:
        verbose_name_plural     = 'Order Headers'
    doc_type                    = models.ForeignKey('generals.DocumentType', on_delete=models.CASCADE)
    doc_serial_number           = models.CharField(max_length=20, unique=True)
    created_by                  = models.CharField(max_length=20)
    department                  = models.CharField(max_length=50)
    branch                      = models.CharField(max_length=50)
    created_date                = models.DateTimeField(default=datetime.now, blank=True)


class OrderDetail(models.Model):
    class Meta:
        verbose_name_plural     = 'Order Details'
    header                   = models.ForeignKey(OrderHeader, on_delete=models.CASCADE)
    container                = models.ForeignKey(Container, on_delete=models.SET_NULL, null=True)
    barcode                  = models.CharField(max_length=20, null=True)
