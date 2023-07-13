from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('profile', views.profile, name='profile'),
    #path('cat_hotels', views.cat_hotels, name='cat_hotels'), change_password

    path('cat_hotel/<int:room_number>/<str:check_in_date>/<str:check_out_date>/', views.cat_hotel, name='cat_hotel'),
    path('completed', views.completed, name='completed'),
    path('edit_completed', views.edit_completed, name='edit_completed'),

    path('cat_hotels/', views.search_available_rooms, name='search_available_rooms'),

    path('calendar/', views.calendar, name='calendar'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('change_password', views.change_password, name='change_password'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    
    path('booking', views.booking, name='booking'),
    path('booking_history', views.booking_history, name='ooking_history'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)