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
    cat_name = models.CharField(max_length=10, null=True, blank=False)
    phone_number = models.CharField(max_length=10, null=True, blank=False)
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

class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    comment = models.CharField(max_length=255, null=True, blank=False)
    rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=False)

    class Meta:
        unique_together = ('customer', 'room')

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
    




