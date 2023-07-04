from rest_framework import serializers
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from cat_hotel.models import *
from .models import *

class manage_cat_hotel(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'description','cat', 'price','image']
        labels = {
            'room_number': 'ห้อง',
            'description': 'รายละเอียด',
            'cat':'จำนวนแมวที่รับได้สูงสุด',
            'price': 'ราคา/บาท',
            'image': 'รูปห้อง'
        }
        widgets = {
            'images': forms.ClearableFileInput(attrs={'multiple': True}),
        }

class EditRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'description', 'price','image']
        labels = {
            'room_number': 'ห้อง',
            'description': 'รายละเอียด',
            'price': 'ราคา/บาท',
            'image': 'รูปห้อง'
        }

class IncomeSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeSummary
        fields = ('id', 'date', 'day_income', 'month_income', 'year_income', 'total_income')

