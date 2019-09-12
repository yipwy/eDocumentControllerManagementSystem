from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Profile(AbstractUser):
    class Meta:
        verbose_name_plural = 'Profiles'
    company                  = models.ForeignKey('generals.Company', on_delete=models.CASCADE)
    contact                  = models.CharField(max_length=35, null=True)
    branch                   = models.ForeignKey('generals.Branch', on_delete=models.CASCADE)
    department               = models.ForeignKey('generals.Department', on_delete=models.CASCADE, blank=True, null=True)
    created_by               = models.CharField(max_length=120)
    modify_by                = models.CharField(max_length=120)
    modify_date              = models.DateTimeField(auto_now=True, null=False)
    is_active                = models.BooleanField(default=False, null=True, blank=True)
    is_superuser             = models.BooleanField(default=False, null=True, blank=True)
    is_staff                 = models.BooleanField(default=False, null=True, blank=True)
    is_documentcontroller    = models.BooleanField(default=False, null=True, blank=True)
    supervisor               = models.ForeignKey('Profile', null=True, on_delete=models.SET_NULL, blank=True)
    email                    = models.CharField(max_length=70, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name