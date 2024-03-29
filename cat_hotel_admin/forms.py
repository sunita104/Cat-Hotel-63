from rest_framework import serializers
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from cat_hotel.models import *
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field



class ManageCatHotelForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'description', 'cat', 'price', 'image']
        labels = {
            'room_number': 'ห้อง',
            'description': 'รายละเอียด',
            'cat': 'จำนวนแมวที่รับได้สูงสุด',
            'price': 'ราคาต่อคืน/บาท',
            'image': 'รูปห้อง'
        }
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }

class EditRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'description', 'price','cat','image']
        labels = {
            'room_number': 'ห้อง',
            'description': 'รายละเอียด',
            'cat': 'จำนวนแมวที่รับได้สูงสุด',
            'price': 'ราคา/บาท',
            'image': 'รูปห้อง'
        }

class AdminEditForm(UserChangeForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        labels = {
            'username': 'ชื่อผู้ใช้แอดมิน',
            'email': 'อีเมล',
            'password': 'รหัสผ่าน',
        }



