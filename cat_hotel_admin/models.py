from django.db import models
from cat_hotel.models import *
from cat_hotel.models import *
from django.urls import reverse
# Create your models here.

class Admin_c(models.Model):
    name = models.CharField(max_length=50, null=True, blank=False)
    username = models.CharField(max_length=50, null=True, blank=False)
    password = models.CharField(max_length=7, null=True, blank=False)

    def __str__(self):
        return self.name
    
class Room(models.Model):
    image = models.FileField(upload_to='rooms/image',null=True, blank=True)
    room_number = models.CharField(max_length=10, null=True, blank=False)
    description = models.TextField(max_length=255, null=True, blank=False)
    cat = models.IntegerField(default=1,null=True, blank=False)
    price = models.IntegerField(null=True, blank=False)

    def __str__(self):
        return self.room_number






