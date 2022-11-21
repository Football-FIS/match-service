from django.db import models

# Create your models here.
class Match(models.Model):
    local: models.CharField(max_length=255)
    visitor: models.CharField(max_length=255)
    alignment: models.CharField(max_length=255)
    url: models.URLField(max_length=200)
    weather: models.CharField(max_length=255)
    start_date: models.DateTimeField()
    created_by_local: models.BooleanField()
    accepted: models.BooleanField()