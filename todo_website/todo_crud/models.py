from django.utils import timezone
from django.db import models

# Create your models here.


class Todo(models.Model):
    done = models.BooleanField()
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True, blank=True)
    created = models.DateTimeField('date created', default=timezone.now)
