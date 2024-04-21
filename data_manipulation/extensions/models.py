from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Document(models.Model):
    name = models.CharField(max_length=200, null=True, unique=True)
    docfile = models.FileField(upload_to='documents')

    def __str__(self):
        return self.name


