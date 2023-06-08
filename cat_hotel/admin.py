from django.contrib import admin

# Register your models here.

from cat_hotel.models import *

admin.site.register(Booking)
admin.site.register(Customer)
admin.site.register(BookingHistory)