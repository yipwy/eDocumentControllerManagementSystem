from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Profile(AbstractUser):
    class Meta:
        verbose_name_plural = 'Profiles'
    company          = models.CharField(max_length=30, unique=True, null=False)
    contact          = models.CharField(max_length=20, null=True)
    branch           = models.ForeignKey('generals.Branch', on_delete=models.CASCADE)
    department       = models.ForeignKey('generals.Department', on_delete=models.CASCADE)
    created_by       = models.CharField(max_length=20)
    modify_by        = models.CharField(max_length=20)
    modify_date      = models.DateTimeField(default=datetime.now, blank=True)
    is_superuser     = models.BooleanField(default=False, null=True, blank=True)
    is_staff         = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.username