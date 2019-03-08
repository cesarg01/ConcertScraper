from django.contrib import admin
from .models import ConcertEvent
# Register your models here.

# Make the model visible on the admin page
admin.site.register(ConcertEvent)