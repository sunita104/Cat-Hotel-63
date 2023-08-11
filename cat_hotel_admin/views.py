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
from django.utils import timezone
from cat_hotel_admin.forms import *
from django.template.loader import render_to_string
import calendar
from django.views import generic
from django.core.exceptions import ObjectDoesNotExist
#from cat_hotel_admin.utils import Calendar
from django.utils.safestring import mark_safe
from django.db.models import Q
from cat_hotel_admin.models import *
from django.db.models import Sum, Max
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
import matplotlib.pyplot as plt
import pandas as pd
import json
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.db import IntegrityError


#admin

@staff_member_required(login_url='admin_login')
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'ผู้ใช้ของคุณถูกปฏิเสธการเข้าใช้ คุณต้องเป็นผู้ดูแลระบบเพื่อเข้าสู่ระบบ')
            return redirect('admin_login')
    else:
        return render(request, 'cat_hotel_admin/admin_login.html')

@staff_member_required(login_url='admin_login')
def profile_admin(request):
    return render(request, 'cat_hotel_admin/profile_admin.html')
           
def admin_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('admin_login')
    else:
        return redirect('admin_login')

@staff_member_required(login_url='admin_login')
def manage_cat_hotel_admin(request):
    if request.method == 'POST':
        form = ManageCatHotelForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('manage_cat_hotel_admin')
            except IntegrityError:
                form.add_error(' ')
    else:
        form = ManageCatHotelForm()

    managed_cat_hotels = Room.objects.all()

    context = {
        "managed_cat_hotels": managed_cat_hotels,
        "form": form
    }

    return render(request, 'cat_hotel_admin/manage_cat_hotel_admin.html', context=context)


@staff_member_required(login_url='admin_login')
def edit_room(request, pk):
    room = get_object_or_404(Room, pk=pk)

    if room.booking_set.exists():
        messages.error(request, "ไม่สามารถแก้ไขห้องที่มีการจองได้")
        return redirect('manage_cat_hotel_admin')

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

@staff_member_required(login_url='admin_login')
def delete_room(request, pk):
    room = get_object_or_404(Room, pk=pk)

    if room.booking_set.exists():
        messages.error(request, "ไม่สามารถลบห้องที่มีการจองได้")
        return redirect('manage_cat_hotel_admin')

    if request.method == 'POST':
        room.delete()
        return redirect('manage_cat_hotel_admin')
    else:
        context = {
            'room': room,
        }
    
    return render(request, 'cat_hotel_admin/manage_cat_hotel_admin.html', context=context)


#calendar_admin

@staff_member_required(login_url='admin_login')
def calendar_admin(requset):
    return render(requset, 'cat_hotel_admin/calendar_admin.html')

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


#show status

@staff_member_required(login_url='admin_login')
def booking_admin(request):
    bookings = Booking.objects.filter(staying_status=False,confirm_status=False)

    context = {
        'bookings': bookings,
        'search_query': ''
    }
    return render(request, 'cat_hotel_admin/booking_admin.html', context=context)

@staff_member_required(login_url='admin_login')
def confirmed_booking_request(requset):
    bookings = Booking.objects.filter(confirm_status=True)

    context = {
        "bookings": bookings
        }
    return render(requset, 'cat_hotel_admin/confirmed_booking_request.html',context=context)

@staff_member_required(login_url='admin_login')
def currently_staying(request):
    bookings = Booking.objects.filter(staying_status=True)

    context = {
        "bookings": bookings
        }
    
    return render(request, "cat_hotel_admin/currently_staying.html", context=context)

@staff_member_required(login_url='admin_login')
def booking_history(request):
    booking_history = BookingHistory.objects.all()

    context = {
        'booking_history': booking_history
        }

    return render(request, 'cat_hotel_admin/booking_history.html', context=context)


#booking_status

@staff_member_required(login_url='admin_login')
def confirm_booking_admin(request, booking_id):
    booking = Booking.objects.get(id=booking_id)

    if booking.staying_status:
        return redirect('booking_admin')

    booking.waiting_confirm = False
    booking.confirm_status = True
    booking.save()
    return redirect('confirmed_booking_request')

@staff_member_required(login_url='admin_login')
def confirm_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)

    if booking.staying_status :
        return redirect('confirmed_booking_request')
    
    booking.waiting_confirm = False
    booking.confirm_status = False
    booking.staying_status = True
    booking.save()

    return redirect('currently_staying')

@staff_member_required(login_url='admin_login')
def end_stay(request, booking_id):  
    booking = Booking.objects.get(id=booking_id)

    booking_history = BookingHistory(
        customer_b=booking.customer,
        room=booking.room,
        start_date=booking.start_date,
        end_date=booking.end_date,
        cat=booking.cat,
        cat_name=booking.cat_name,
        total_price=booking.total_price,
        phone_number=booking.phone_number,
        checked_out=True
    )
    booking_history.save()

    booking.room.available = True
    booking.room.save()

    booking.delete()

    return redirect('booking_history')

@staff_member_required(login_url='admin_login')
def cancel_booking_admin(request, booking_id):
    if request.method == 'POST':
        booking = Booking.objects.get(id=booking_id)
        reason_text = request.POST.get('reason_text')

        cancellation_reason = CancellationReason(
            customer=booking.customer,
            room=booking.room,
            start_date=booking.start_date,
            end_date=booking.end_date,
            cat=booking.cat,
            cat_name=booking.cat_name,
            total_price=booking.total_price,
            phone_number=booking.phone_number,
            reason_text=reason_text
        )

        cancellation_reason.save()
        booking.delete()
        return redirect('booking_admin')

    return render(request, 'cat_hotel_admin/cancel_booking_admin.html')
     

#dashboard

def calculate_income_summary():
    today = date.today()
    day_income = Booking.objects.filter(start_date=today, staying_status=True).aggregate(Sum('total_price'))['total_price__sum'] or 0.0
    month_income = BookingHistory.objects.filter(start_date__month=today.month, checked_out=True).aggregate(Sum('total_price'))['total_price__sum'] or 0.0
    year_income = BookingHistory.objects.filter(start_date__year=today.year, checked_out=True).aggregate(Sum('total_price'))['total_price__sum'] or 0.0
    total_income = BookingHistory.objects.filter(checked_out=True).aggregate(Sum('total_price'))['total_price__sum'] or 0.0

    income_summary, created = IncomeSummary.objects.get_or_create(date=today)
    income_summary.day_income = day_income
    income_summary.month_income = month_income
    income_summary.year_income = year_income
    income_summary.total_income = total_income
    income_summary.save()

    return income_summary

@staff_member_required(login_url='admin_login')
def dashboard(request):
    all_months = list(calendar.month_name)[1:]
    income_summaries = IncomeSummary.objects.order_by('date')

    selected_year = request.GET.get('year')
    if selected_year:
        income_summaries = income_summaries.filter(date__year=selected_year)

    monthly_income_data = [0] * 12
    months = []

    for month in range(1, 13):
        matching_summary = income_summaries.filter(date__month=month).last()
        if matching_summary:
            monthly_income_data[month - 1] = matching_summary.month_income
        months.append(all_months[month - 1])

    total_income = income_summaries.last().year_income if income_summaries.exists() else 0
    income_summary = calculate_income_summary()

    context = {
        'income_summary': income_summary,  
        'monthly_income_data': json.dumps(monthly_income_data),
        'months': json.dumps(months),
        "selected_year": selected_year,
        'total_income': total_income,
    }

    return render(request, 'cat_hotel_admin/dashboard.html', context=context)


#search fution

@staff_member_required(login_url='admin_login')
def search_booking_admin(request):
    search_query = request.GET.get('query')
    bookings = Booking.objects.filter(staying_status=False, confirm_status=False)

    if search_query:
        bookings = bookings.filter(
            Q(customer__username__icontains=search_query) |
            Q(room__room_number__icontains=search_query) |
            Q(customer__first_name__icontains=search_query) |
            Q(customer__last_name__icontains=search_query) |
            Q(cat_name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(start_date__icontains=search_query) |
            Q(end_date__icontains=search_query)
        )

    context = {
        'bookings': bookings,
        'search_query': search_query
    }

    return render(request, 'cat_hotel_admin/booking_admin.html', context=context)

@staff_member_required(login_url='admin_login')
def search_confirm_booking_admin(request):
    search_query = request.GET.get('query')
    bookings = Booking.objects.filter(confirm_status=True)

    if search_query:
        bookings = bookings.filter(
            Q(customer__username__icontains=search_query) |
            Q(room__room_number__icontains=search_query) |
            Q(customer__first_name__icontains=search_query) |
            Q(customer__last_name__icontains=search_query) |
            Q(cat_name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(start_date__icontains=search_query) |
            Q(end_date__icontains=search_query)
        )

    context = {
        'bookings': bookings,
        'search_query': search_query
    }

    return render(request, 'cat_hotel_admin/confirmed_booking_request.html', context=context)


@staff_member_required(login_url='admin_login')
def search_currently_staying(request):
    search_query = request.GET.get('query')
    bookings = Booking.objects.filter(staying_status=True)

    if search_query:
        bookings = bookings.filter(
            Q(customer__username__icontains=search_query) |
            Q(room__room_number__icontains=search_query) |
            Q(customer__first_name__icontains=search_query) |
            Q(customer__last_name__icontains=search_query) |
            Q(cat_name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(start_date__icontains=search_query) |
            Q(end_date__icontains=search_query)
        )

    context = {
        "bookings": bookings,
        'search_query': search_query
    }

    return render(request, "cat_hotel_admin/currently_staying.html", context=context)

@staff_member_required(login_url='admin_login')
def search_booking_history(request):
    search_query = request.GET.get('query')
    booking_history = BookingHistory.objects.all()

    if search_query:
        booking_history = booking_history.filter(
            Q(customer_b__username__icontains=search_query) |
            Q(room__room_number__icontains=search_query) |
            Q(customer_b__first_name__icontains=search_query) |
            Q(customer_b__last_name__icontains=search_query) |
            Q(cat_name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(start_date__icontains=search_query) |
            Q(end_date__icontains=search_query)
        )

    context = {
        'booking_history': booking_history,
        'search_query': search_query
    }

    return render(request, 'cat_hotel_admin/booking_history.html', context=context)

@staff_member_required(login_url='admin_login')
def search_canceled_booking(request):
    search_query = request.GET.get('query')
    canceled_bookings = CancellationReason.objects.all()

    if search_query:
        canceled_bookings = canceled_bookings.filter(
            Q(customer__username__icontains=search_query) |
            Q(room__room_number__icontains=search_query) |
            Q(customer__first_name__icontains=search_query) |
            Q(customer__last_name__icontains=search_query) |
            Q(cat_name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
             Q(start_date__icontains=search_query) |
            Q(end_date__icontains=search_query)
        )

    context = {
        'canceled_bookings': canceled_bookings,
        'search_query': search_query
    }
    return render(request, 'cat_hotel_admin/canceled_booking.html', context)

@staff_member_required(login_url='admin_login')
def search_customer(request):
    search_query = request.GET.get('query', '')
    customers = get_user_model().objects.filter(
        Q(username__icontains=search_query) |
        Q(first_name__icontains=search_query) |
        Q(last_name__icontains=search_query),
        is_staff=False
    )
    context = {
        'customers': customers,
        'search_query': search_query
    }
    return render(request, 'cat_hotel_admin/customer.html', context)

#costomer

@staff_member_required(login_url='admin_login')
def customer(request):
    User = get_user_model()
    customers = User.objects.filter(is_superuser=False)
    
    context = {
        'customers': customers
    }

    return render(request, 'cat_hotel_admin/customer.html', context)


#cancel booking

@staff_member_required(login_url='admin_login')
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
 
        booking.status = 'canceled'
        booking.save()
        return redirect('booking_history')  

    context = {
        'booking': booking
    }
    return render(request, 'cat_hotel_admin/cancel_booking.html', context)

@staff_member_required(login_url='admin_login')
def canceled_booking(request):
    canceled_bookings = CancellationReason.objects.all()

    context = {
        'canceled_bookings': canceled_bookings,
    }
    return render(request, 'cat_hotel_admin/canceled_booking.html', context)

    
'''
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard')  # Replace 'admin_dashboard' with the URL name of your admin dashboard page
        else:
            # Handle invalid login or unauthorized access
            return render(request, 'admin_view.html', {'error_message': 'Invalid login or unauthorized access.'})
    else:
        return render(request, 'cat_hotel_admin/admin_view.html')

'''

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

