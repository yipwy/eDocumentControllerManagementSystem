from django.db import models
from datetime import datetime


# Create your models here.
class Profile(models.Model):
    class Meta:
        verbose_name_plural = 'Profiles'
    companyId        = models.CharField(max_length=50)
    departmentId     = models.CharField(max_length=50)
    is_active        = models.BooleanField(default=False)
    created_by       = models.CharField(max_length=20)
    created_date     = models.DateTimeField(default=datetime.now(), blank=True)
    modify_by        = models.CharField(max_length=20)
    modify_date      = models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self):
        return self.companyId