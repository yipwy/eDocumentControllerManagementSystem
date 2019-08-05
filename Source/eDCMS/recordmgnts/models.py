from django.db import models
from simple_history.models import HistoricalRecords
from datetime import *


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
    department                  = models.ForeignKey('generals.Department', on_delete=models.CASCADE, null=True)
    history = HistoricalRecords(table_name='container_history')

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


class ContainerInstance(models.Model):
    class Meta:
        verbose_name_plural     = 'Container Instances'
    container = models.ForeignKey(Container, on_delete=models.SET_NULL, null=True)
    due_date  = models.DateField(null=True)
    user      = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    status    = models.BooleanField(null=True)

    @property
    def is_overdue(self):
        if date.today() > self.due_date:
            return True
        return False
