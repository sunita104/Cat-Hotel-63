from django.db import models
from cat_hotel.models import *
from cat_hotel.models import *
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

 

class Room(models.Model):
    image = models.FileField(upload_to='rooms/image',null=True, blank=True)
    room_number = models.CharField(max_length=10, unique=True, null=True, blank=False)
    description = models.TextField(max_length=255, null=True, blank=False)
    cat = models.IntegerField(default=1,null=True, blank=False)
    price = models.IntegerField(null=True, blank=False)

    def __str__(self):
        return self.room_number

class IncomeSummary(models.Model):
    date = models.DateField(default=timezone.now, null=True, blank=False)
    day_income = models.FloatField(default=0, null=True, blank=False)
    month_income = models.FloatField(default=0, null=True, blank=False)
    year_income = models.FloatField(default=0, null=True, blank=False)
    total_income = models.FloatField(default=0, null=True, blank=False)

    def update_summary(self, amount):
        self.day_income += amount
        self.month_income += amount
        self.year_income += amount
        self.total_income += amount
        self.save()








    







