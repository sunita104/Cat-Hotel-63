from django.contrib.auth import views 
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.admin_login, name='admin_login'),  
    path('dashboard/', views.dashboard, name='dashboard'),
    path('manage_cat_hotel_admin', views.manage_cat_hotel_admin, name='manage_cat_hotel_admin'),
    path('manage_cat_hotel_admin/<int:pk>/', views.delete_room, name='delete_room'),
    path('booking_admin', views.booking_admin, name='booking_admin'),
    path('currently_staying/', views.currently_staying, name='currently_staying'),
    path('currently_staying/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),   
    path('booking_history/<int:booking_id>/', views.end_stay, name='end_stay'),
    path('booking_history/', views.booking_history, name='booking_history'),
    path('calendar_admin/', views.calendar_booking, name='calendar_booking'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('edit_room_cat_hotel/<int:pk>/', views.edit_room, name='edit_room'),
    path('confirmed_booking_request/', views.confirmed_booking_request, name='confirmed_booking_request'),
    path('confirmed_booking_request/<int:booking_id>/', views.confirm_booking_admin, name='confirm_booking_admin'),

    

]