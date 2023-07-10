from rest_framework import serializers
from django import forms
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
            'price': 'ราคา/บาท',
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

class ManageWebpageForm(forms.Form):
    title = forms.CharField(label='หัวข้อหน้าเว็บ', max_length=100)
    image1 = forms.ImageField(label='รูปภาพสไลด์1')
    image2 = forms.ImageField(label='รูปภาพสไลด์2')
    image3 = forms.ImageField(label='รูปภาพสไลด์3')  
    description1 = forms.CharField(label='รายละเอียดหัวข้อ', widget=forms.Textarea)
    image4 = forms.ImageField(label='รูปภาพแนะนำ')
    description2 = forms.CharField(label='รายละเอียดแนะนำ', widget=forms.Textarea)
    about_us = forms.CharField(label='เกี่ยวกับ')
    location = forms.CharField(label='สถานที่')
    contact = forms.CharField(label='ติดต่อ')


