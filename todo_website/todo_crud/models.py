from django.db import models

# Create your models here.


class Todo(models.Model):
    done = models.BooleanField()
    title = models.CharField(max_length=100)
