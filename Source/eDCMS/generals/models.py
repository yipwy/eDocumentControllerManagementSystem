from django.db import models
from datetime import datetime


class DocumentType(models.Model):
    class Meta:
        verbose_name_plural = 'DocumentTypes'

    document_code = models.CharField(max_length=20, unique=True)
    document_description = models.CharField(max_length=50)
    # document_number_seriesId = models.ForeignKey('SeriesNumber', null=True, blank=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    # created_by = models.CharField(max_length=20)
    created_date = models.DateTimeField(default=datetime.now, blank=True)
    # modify_by = models.CharField(max_length=20)
    # modify_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.document_description


# class SeriesNumber(models.Model):
#     class Meta:
#         verbose_name_plural = 'SeriesNumbers'
#
#     series_code = models.CharField(max_length=20, unique=True)
#     # series_description = models.CharField(max_length=50)
#     starting_number = models.IntegerField(default=1)
#     ending_number = models.IntegerField(default=9999)
#     next_number = models.IntegerField()
#     is_active = models.BooleanField(default=False)
#     created_by = models.CharField(max_length=20)
#     created_date = models.DateTimeField(default=datetime.now, blank=True)
#     # modify_by = models.CharField(max_length=20)
#     # modify_date = models.DateTimeField(default=datetime.now, blank=True)
#
#     def __str__(self):
#         return self.series_code


class Branch(models.Model):
    class Meta:
        verbose_name_plural     = "Branches"
    branch                      = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.branch


class Company(models.Model):
    class Meta:
        verbose_name_plural     = "Companies"
    company                     = models.CharField(max_length=55, null=True)

    def __str__(self):
        return self.company


class Department(models.Model):
    class Meta:
        verbose_name_plural     = "Departments"
    department                  = models.CharField(max_length=55, null=True)
    branch                      = models.ForeignKey('Branch', on_delete=models.CASCADE)

    def __str__(self):
        return self.department


class Warehouse(models.Model):
    class Meta:
        verbose_name_plural     = "Warehouses"
    warehouse_id                = models.CharField(max_length=55, null=False, unique=False)
    branch                      = models.ForeignKey('Branch', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.branch) + " - " + str(self.warehouse_id)


class Bay(models.Model):
    class Meta:
        verbose_name_plural     = "Locations"
    bay_id                 = models.CharField(max_length=20, null=True, unique=False)
    warehouse                   = models.ForeignKey('Warehouse', on_delete=models.CASCADE)

    def __str__(self):
        return self.bay_id
