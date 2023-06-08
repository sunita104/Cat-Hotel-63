from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from cat_hotel_admin.models import *
from cat_hotel.forms import *
from django.db.models import Q
from django.utils import timezone
from cat_hotel.models import *
from datetime import datetime, timedelta, date
from cat_hotel_admin.views import calendar_booking

# Create your views here.

def home(requset):
    return render(requset, 'cat_hotel/home.html')

def about(requset):
    return render(requset, 'cat_hotel/about.html')

def profile(requset):
    return render(requset, 'cat_hotel/profile.html')


def cat_hotel(request, room_number, check_in_date, check_out_date):
    one_room = Room.objects.get(room_number=room_number)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = Booking.objects.create(
                room=one_room,
                customer=form.cleaned_data['customer'],
                start_date=datetime.strptime(check_in_date, '%Y-%m-%d').date(),
                end_date=datetime.strptime(check_out_date, '%Y-%m-%d').date(),
                cat_name=form.cleaned_data['cat_name'],
                phone_number=form.cleaned_data['phone_number']
            )
            booking.save()
        
            return redirect('cat_hotel', booking_id=booking.id)
    
    else:
        form = BookingForm(initial={
            'start_date': datetime.strptime(check_in_date, '%Y-%m-%d').date(),
            'end_date': datetime.strptime(check_out_date, '%Y-%m-%d').date(),
        })
    
    context = {
        "one_room": one_room,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "form": form,
    }

    return render(request, 'cat_hotel/cat_hotel.html', context)


def search_available_rooms(request):
    if request.method == 'GET':
        check_in_date = request.GET.get('check_in_date') 
        check_out_date = request.GET.get('check_out_date')
        initial_values = {'check_in_date': check_in_date, 'check_out_date': check_out_date}
        form = SearchForm(initial=initial_values)
           
        if check_in_date and check_out_date:
            overlapping_bookings = Booking.objects.filter(start_date__lte=check_out_date, end_date__gte=check_in_date) 
            booked_rooms = [booking.room for booking in overlapping_bookings] 
            available_rooms = Room.objects.exclude(id__in=[room.id for room in booked_rooms]) 
           
            for room in available_rooms:
                num_days = (datetime.strptime(check_out_date, '%Y-%m-%d').date() - datetime.strptime(check_in_date, '%Y-%m-%d').date()).days 
                if num_days > 0:
                    total_price = num_days * room.price
                    room.total_price = total_price
                else:
                    total_price = room.price

            context = { 
                'form': form,
                'available_rooms': available_rooms,
                'check_in_date': check_in_date,
                'check_out_date': check_out_date,

            }
            return render(request, 'cat_hotel/cat_hotels.html', context=context)
        else:
            form = SearchForm()
            return render(request, 'cat_hotel/cat_hotels.html', {'form': form})


def completed(request):
    booking = Booking.objects.all()

    context = {
        'booking': booking
    }
    return render(request, 'cat_hotel/completed.html', context=context)

def calendar(request):
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
    return render(request,'cat_hotel/calendar.html',context)

def edit(request):
    return render(request, 'cat_hotel/completed.html')
    
def success(request):
    return render(request, 'success.html')


def edit_completed(requset):
    return render(requset,'cat_hotel/edit_completed.html')



