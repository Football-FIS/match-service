from django.db import models
from django.utils.crypto import get_random_string

# Create your models here.
class Match(models.Model):
    id = models.CharField(primary_key=True, max_length=24, default=get_random_string(length=24))
    
    local = models.CharField(max_length=255)
    visitor = models.CharField(max_length=255)
    alignment = models.CharField(max_length=255)
    url = models.URLField(max_length=200)
    city =models.CharField(max_length=50)
    weather = models.CharField(max_length=255, null=True)
    start_date = models.DateTimeField()
    created_by_local = models.BooleanField()
    accepted = models.BooleanField()