from django.db import models
from cat_hotel_admin.models import *
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=False)
    start_date = models.DateField(null=True, blank=False)
    end_date = models.DateField(null=True, blank=False)
    #cat = models.IntegerField(default=1,null=True, blank=False)
    cat_name = models.CharField(max_length=10, null=True, blank=False)
    phone_number = models.CharField(max_length=10, null=True, blank=False)
    total_price = models.IntegerField(null=True, blank=False)
    waiting_confirm = models.BooleanField(default=True, null=True, blank=False)
    confirm_status = models.BooleanField(default=False, null=True, blank=False)
    staying_status = models.BooleanField(default=False, null=True, blank=False)

    def save(self, *args, **kwargs):
        self.start_date = datetime.datetime.strptime(self.start_date.strftime('%Y-%m-%d'), '%Y-%m-%d').date()
        self.end_date = datetime.datetime.strptime(self.end_date.strftime('%Y-%m-%d'), '%Y-%m-%d').date()

        if self.pk:
            old_booking = Booking.objects.get(pk=self.pk)
            if old_booking.staying_status and not self.staying_status:
                self.room.available = True
        else:
            self.room.available = False
        self.room.save()
        super(Booking, self).save(*args, **kwargs)

class CancellationReason(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=False)
    start_date = models.DateField(null=True, blank=False)
    end_date = models.DateField(null=True, blank=False)
    cat_name = models.CharField(max_length=10, null=True, blank=False)
    cat = models.IntegerField(null=True, blank=False)
    phone_number = models.CharField(max_length=10, null=True, blank=False)
    reason_text = models.TextField()

    def __str__(self):
        return self.reason_text


class BookingHistory(models.Model):
    customer_b = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=False)
    start_date = models.DateField(null=True, blank=False)
    end_date = models.DateField(null=True, blank=False)
    cat_name = models.CharField(max_length=10, null=True, blank=False)
    cat = models.IntegerField(null=True, blank=False)
    phone_number = models.CharField(max_length=10, null=True, blank=False)
    checked_out = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return self.room.room_number





