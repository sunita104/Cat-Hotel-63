from django.contrib.auth import views 
from django.urls import path
from . import views
from .views import *
from django.shortcuts import render




urlpatterns = [
    path('', views.admin_login, name='admin_login'),  
    path('graph/', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    #path('dashboard/', views.income_summary_graph, name='income_summary_graph'),
    #path('graph/', views.income_summary_graph, name='income_summary_graph'),
    #path('api', views.ChartData.as_view(), name='chart_data'),
    #path('chart', line_chart, name='line_chart'),
    #path('chartJSON', line_chart_json, name='line_chart_json'),
    #path('dashboard/', views.get_chart_data, name='get_chart_data'),
    path('manage_cat_hotel_admin', views.manage_cat_hotel_admin, name='manage_cat_hotel_admin'),
    path('manage_cat_hotel_admin/<int:pk>/', views.delete_room, name='delete_room'),
    path('booking_admin', views.booking_admin, name='booking_admin'),
    path('currently_staying', views.currently_staying, name='currently_staying'),
    path('currently_staying/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),   
    path('booking_history/<int:booking_id>/', views.end_stay, name='end_stay'),
    path('booking_history', views.booking_history, name='booking_history'),
    path('calendar_admin/', views.calendar_booking, name='calendar_booking'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('edit_room_cat_hotel/<int:pk>/', views.edit_room, name='edit_room'),
    path('confirmed_booking_request', views.confirmed_booking_request, name='confirmed_booking_request'),
    path('confirmed_booking_request/<int:booking_id>/', views.confirm_booking_admin, name='confirm_booking_admin'),

    #search 
    path('booking_admin/', views.search_booking_admin, name='search_booking_admin'),
    path('confirmed_booking_request/', views.search_confirm_booking_admin, name='search_confirm_booking_admin'),
    path('currently_staying/', views.search_currently_staying, name='search_currently_staying'),
    path('booking_history/', views.search_booking_history, name='search_booking_history'),
    path('search_customer/', views.search_customer, name='search_customer'),

    #customer 
    path('customer', views.customer, name='customer'),
    #path('edit_web_page_admin', views.edit_web_page, name='web_page_admin'),

    #admin
    path('admin_login', views.admin_login, name='admin_login'),
    path('profile_admin', views.profile_admin, name='profile_admin'),

    #CancellationReason
    path('cancel_booking_admin/<int:booking_id>/', views.cancel_booking_admin, name='cancel_booking_admin'),
    







    

]

