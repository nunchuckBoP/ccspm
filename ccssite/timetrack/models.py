from django.conf import settings
from django.db import models

# Create your models here.
class TimeSheet(models.Model):
    created_on = models.DateField(verbose_name='Created On')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
