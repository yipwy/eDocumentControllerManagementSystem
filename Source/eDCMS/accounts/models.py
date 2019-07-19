from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Profile(AbstractUser):
    class Meta:
        verbose_name_plural = 'Profiles'
    companyId        = models.CharField(max_length=50)
    contact          = models.CharField(max_length=20, null=True)
    branchId         = models.CharField(max_length=20)
    departmentId     = models.CharField(max_length=50)
    created_by       = models.CharField(max_length=20)
    modify_by        = models.CharField(max_length=20)
    modify_date      = models.DateTimeField(default=datetime.now, blank=True)
    is_superuser     = models.BooleanField(default=False, null=True, blank=True)
    is_staff         = models.BooleanField(default=False, null=True, blank=True)


    def __str__(self):
        return self.username