from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cat_hotel.models import *
from cat_hotel_admin.forms import *
from datetime import datetime, timedelta, date
from itertools import groupby
from cat_hotel_admin.forms import *
from django.template.loader import render_to_string
import calendar
from django.views import generic
from cat_hotel_admin.utils import Calendar
from django.utils.safestring import mark_safe
from django.db.models import Q

# Create your views here.

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    else:
        return render(request, 'cat_hotel_admin/admin_login.html')
           
def admin_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('admin_login')

def dashboard(requset):
    return render(requset, 'cat_hotel_admin/dashboard.html')

def manage_cat_hotel_admin(request):
    if request.method == 'POST':
        form = manage_cat_hotel(request.POST, request.FILES)  # request.FILES อัพรูป
        if form.is_valid():
            form.save()
            return redirect('manage_cat_hotel_admin')
    else:
        form = manage_cat_hotel()

    managed_cat_hotels = Room.objects.all()

    context = {
        "managed_cat_hotels": managed_cat_hotels,
        "form": form
    }

    return render(request, 'cat_hotel_admin/manage_cat_hotel_admin.html', context=context)


def edit_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = EditRoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('manage_cat_hotel_admin')
    else:
        form = EditRoomForm(instance=room)
    
    context = {
        "form": form
    }
        
    return render(request, 'cat_hotel_admin/edit_room_cat_hotel.html', context=context)

def delete_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('manage_cat_hotel_admin')
    else:
        context = {
            'room': room,
        }
        return render(request,'cat_hotel_admin/manage_cat_hotel_admin.html', context=context)

def calendar_booking(request):
    all_booking = Booking.objects.all()
    get_booking_types = Booking.objects.only('booking_type')

    if request.GET:  
        booking_arr = []
        if request.GET.get('booking_type') == "all":
            all_booking = Booking.objects.all()
        else:   
            all_booking = Booking.objects.filter(booking_type__icontains=request.GET.get('booking_type'))
        
        for i in all_booking:
            booking_sub = {}
            booking_sub['title'] = i.room.room_number
            start_date = datetime.datetime.strptime(str(i.start_date.date()), "%d-%m-%Y").strftime("%d-%m-%Y")
            end_date = (datetime.datetime.strptime(str(i.end_date.date()), "%Y-%m-%d") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            booking_sub['start'] = start_date
            booking_sub['end'] = end_date
            booking_arr.append(booking_sub)
        return HttpResponse(json.dumps(booking_arr))

    context = {
        "all_booking":all_booking,
        "get_booking_types":get_booking_types,

    }
    return render(request,'cat_hotel_admin/calendar_admin.html',context=context)

def booking_admin(request):
    booking = Booking.objects.filter(staying_status=False,confirm_status=False)

    context = {
        'booking': booking
    }
    return render(request, 'cat_hotel_admin/booking_admin.html', context=context)

def confirmed_booking_request(requset):
    bookings = Booking.objects.filter(confirm_status=True)

    context = {
        "bookings": bookings
        }
    return render(requset, 'cat_hotel_admin/confirmed_booking_request.html',context=context)

def currently_staying(request):
    bookings = Booking.objects.filter(staying_status=True)

    context = {
        "bookings": bookings
        }
    
    return render(request, "cat_hotel_admin/currently_staying.html", context=context)

def booking_history(request):
    booking_history = BookingHistory.objects.all()

    context = {
        'booking_history': booking_history
        }

    return render(request, 'cat_hotel_admin/booking_history.html', context=context)

def confirm_booking_admin(request, booking_id):
    booking = Booking.objects.get(id=booking_id)

    if booking.staying_status :
        return redirect('booking_admin')

    booking.confirm_status = True
    booking.save()
    return redirect('confirmed_booking_request')

def confirm_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)

    if booking.staying_status :
        return redirect('confirmed_booking_request')
        
    booking.confirm_status = False
    booking.staying_status = True
    booking.save()

    return redirect('currently_staying')

def end_stay(request, booking_id):  
    booking = Booking.objects.get(id=booking_id)

    booking_history = BookingHistory(
        customer_b=booking.customer,
        room=booking.room,
        start_date=booking.start_date,
        end_date=booking.end_date,
        cat_name=booking.cat_name,
        phone_number=booking.phone_number,
        checked_out=True
    )
    booking_history.save()

    booking.room.available = True
    booking.room.save()

    booking.delete()

    return redirect('booking_history')


def calendar_admin(requset):
    return render(requset, 'cat_hotel_admin/calendar_admin.html')


'''
class CalendarView(generic.ListView):
    model = Booking
    template_name = 'cat_hotel_admin/calendar_admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))
        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
    
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return date.today()

# เดือนก่อนหน้า
def prev_month(d):
    first = d.replace(day=1) # ให้ตัวแปรนี้เท่ากับวันที่ที่ส่งเข้ามา (d) เท่ากับวันแรกของเดือนที่รับมา
    prev_month = first - timedelta(days=1) # ลบจำนวนวันที่ 1 จากวันแรกของเดือนนั้นด้วย timedelta(days=1) เพื่อให้ได้วันก่อนหน้าเดือนนั้น
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    # เอาปีและเดือนของวันก่อนหน้า ทำให้เป็นสตริง แล้วรีเทิร์นออกไปด้วยจ้า
    return month

# เดือนถัดไป
def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month
'''
