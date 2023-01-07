from django.db import models
from django.utils.crypto import get_random_string

# Create your models here.
class Match(models.Model):
    id = models.CharField(primary_key=True, max_length=24, default=get_random_string(length=24))
    user_uid = models.CharField(max_length=255)
    local = models.CharField(max_length=255)
    visitor = models.CharField(max_length=255)
    alignment = models.CharField(max_length=255)
    url = models.URLField(max_length=200, unique=True)
    city =models.CharField(max_length=50)
    weather = models.CharField(max_length=255, null=True)
    start_date = models.DateTimeField()
    sent_email = models.BooleanField()