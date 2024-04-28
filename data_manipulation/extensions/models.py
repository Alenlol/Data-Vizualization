from django.db import models
from django.core.validators import FileExtensionValidator
from django.conf import settings


# Create your models here.
class Document(models.Model):
    name = models.CharField(max_length=200, null=True, unique=True)
    docfile = models.FileField(
        upload_to=str(settings.BASE_DIR).split('\\')[-1] + '/static/data_collection',
        validators=[FileExtensionValidator(allowed_extensions=["csv"])]
    )

    def __str__(self):
        return self.name


