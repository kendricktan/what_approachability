from __future__ import unicode_literals

from django.db import models

# Create your models here.
class tandaAccount(models.Model):
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=50)
