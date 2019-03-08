from django.conf import settings
from django.db import models
from django.utils import timezone
# Create your models here.

class ConcertEvent(models.Model):
    # artist has many tour dates
    artist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    
    

class Weather(models.Model):

    cold = models.CharField(max_length=200)
    def __str__(self):
        return self.title