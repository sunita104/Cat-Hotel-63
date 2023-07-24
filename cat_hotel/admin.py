from django.contrib import admin

# Register your models here.

from cat_hotel.models import *

admin.site.register(Booking)
admin.site.register(BookingHistory)
admin.site.register(CancellationReason)