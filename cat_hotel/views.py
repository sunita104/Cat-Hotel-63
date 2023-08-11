from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from cat_hotel_admin.models import *
from cat_hotel.forms import *
from django.db.models import Q
from django.utils import timezone
from cat_hotel.models import *
from datetime import datetime, timedelta, date
from cat_hotel_admin.views import calendar_booking
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import QueryDict

# Create your views here.

def home(request):
    room = Room.objects.all()

    context = {

     "room": room,
    }

    return render(request, 'cat_hotel/home.html', context=context)

def about(requset):
    return render(requset, 'cat_hotel/about.html')

def profile(requset):
    return render(requset, 'cat_hotel/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'cat_hotel/edit_profile.html', context)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Replace 'home' with your desired URL
    else:
        form = LoginForm(request)

    context = {
        'form': form,
    }

    return render(request, 'cat_hotel/login.html', context=context)

@login_required
def change_password(request):
    form = PasswordChangeForm(request.user)

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            return redirect('profile')  

    context = {
        'form': form,
    }

    return render(request, 'cat_hotel/change_password.html', context=context)
def logout_view(request):
    logout(request)
    return redirect('home')  

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'คุณ {username} สมัครสามชิกสำเร็จ')
            return redirect('login')  
    else:
        form = RegisterForm()

    return render(request, 'cat_hotel/register.html', {'form': form})


# booking_

@login_required
def booking_cat_hotel(request, room_number, check_in_date, check_out_date):
    one_room = Room.objects.get(room_number=room_number)
    num_days = (datetime.strptime(check_out_date, '%Y-%m-%d').date() - datetime.strptime(check_in_date, '%Y-%m-%d').date()).days
    total_price = num_days * one_room.price

    if request.method == 'POST':
        cat_name = request.POST.get('cat_name')
        phone_number = request.POST.get('phone_number')
        start_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()
        total_price = total_price

        if int(request.POST.get('cat', 1)) > one_room.cat:
            messages.error(request, 'จำนวนแมวเกินจำนวนสูงสุดที่อนุญาตในห้องพักแมว')
            return render(request, 'cat_hotel/cat_hotel.html', {
                "customer": request.user,
                "one_room": one_room,
                "check_in_date": check_in_date,
                "check_out_date": check_out_date,
                "total_price": total_price,
            })

        booking = Booking(
            customer=request.user,
            room=one_room,
            cat=int(request.POST.get('cat', 1)),
            cat_name=cat_name,
            phone_number=phone_number,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
            waiting_confirm=True,
            confirm_status=False,
            staying_status=False,
        )
        booking.save()
        return redirect('completed')

    context = {
        "customer": request.user,
        "one_room": one_room,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "total_price": total_price,
    }
    return render(request, 'cat_hotel/cat_hotel.html', context=context)


@login_required
def completed(request):
    booking = Booking.objects.filter(customer=request.user)

    context = {
        'booking': booking
    }
    return render(request, 'cat_hotel/completed.html', context=context)

@login_required
def edit_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    if booking.confirm_status:
        messages.error(request, 'การจองนี้ได้รับการยืนยันแล้วและไม่สามารถแก้ไขได้')
        return redirect('completed')

    elif booking.staying_status:
        messages.error(request, 'การจองนี้ได้รับการยืนยันการเข้าพักแล้วและไม่สามารถแก้ไขได้')
        return redirect('completed')
    
    if request.method == 'POST':
        cat_name = request.POST.get('cat_name')
        phone_number = request.POST.get('phone_number')
        new_cat = int(request.POST.get('cat', 1))

        if new_cat > booking.room.cat:
            messages.warning(request, 'ไม่สามารถแก้ไขได้เนื่องจากจำนวนแมวเกินจำนวนสูงสุดที่อนุญาตในห้องพักแมว')
            return redirect('completed')

        booking.cat_name = cat_name
        booking.phone_number = phone_number
        booking.cat = new_cat
        booking.save()

        return redirect('completed')

    context = {
        'booking': booking,
    }
    return render(request, 'cat_hotel/edit_booking.html', context)


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    if booking.staying_status:
        messages.error(request, 'การจองนี้ได้รับการยืนยันการเข้าพักแล้วและไม่สามารถยกเลิกได้')
        return redirect('completed')

    if request.method == 'POST':
        booking.delete()
        return redirect('completed')

    context = {
        'booking': booking,
    }
    return render(request, 'cat_hotel/completed.html', context)

@login_required
def book_history(request):
    book_history = BookingHistory.objects.filter(customer_b=request.user)
    cancellation_reason = CancellationReason.objects.filter(customer=request.user)

    context = {
        'book_history': book_history,
        'cancellation_reason': cancellation_reason
    }
    return render(request, 'cat_hotel/book_history.html', context)


@login_required
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

#calendar
@login_required
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


def edit_completed(requset):
    return render(requset,'cat_hotel/edit_completed.html')

def booking(requset): 
    return render(requset,'cat_hotel/booking.html')


def cat_hotel(requset): 
    return render(requset,'cat_hotel/cat_hotel.html')









